from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View

from dashboard.forms import ApplicationForm, ApplicationRankForm
from dashboard.models import (Application, ApplicationDocument,
                              ApplicationDocumentType, ApplicationRank,
                              Notification, Rank, Sms)
from dashboard.utils.constants import (APPLICATION_PROCESSED_MESSAGE,
                                       APPLICATION_SUBMISSION_MESSAGE,
                                       APPLICATION_SUBMISSION_SUBJECT)
from dashboard.utils.functions import send_sms
from pension.utils.constants import ApplicationStatus
from setup.models import RetirementReason
import logging

logger = logging.getLogger("django")


class IndexView(View):
    template_name = 'dashboard/index.html'

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)


class NotificationsView(View):
    template_name = 'dashboard/notifications.html'

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)


class NewApplicationFormOneView(PermissionRequiredMixin, View):
    """Create and update applications here.
    """
    template_name = 'dashboard/form_one.html'
    form_class = ApplicationForm
    permission_required = ("dashboard.change_application", )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        application_id = request.GET.get("application_id")
        application = Application.objects.filter(id=application_id).first()
        # Edit only draft and applications in need of changes
        if application and not application.can_edit():
            messages.warning(request, "Editing this application is forbidden.")
            return redirect(
                request.META.get("HTTP_REFERER") or "dashboard:index")

        context = {
            "application": application,
            "ranks": Rank.objects.all(),
            "reasons": RetirementReason.objects.all(),
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        application_id = request.GET.get("application_id")
        application = Application.objects.filter(id=application_id).first()

        if application and not application.can_edit():
            messages.warning(request, "Editing this application is forbidden.")
            return redirect(request.META.get("HTTP_REFERER"))

        form = self.form_class(request.POST,
                               request.FILES or None,
                               instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.last_updated_by = request.user
            if not application_id:
                application.created_by = request.user
            application.save()
            messages.info(request, "Application has been saved")
            return redirect("dashboard:application_form_one_upload",
                            application.id)
        else:
            for field, error in form.errors.items():
                message = f"{field.title()}: {strip_tags(error)}"
                break
            context = {k: v for k, v in request.POST.items()}
            messages.warning(request, message)
            return render(request, self.template_name, context)


class NewApplicationAddRanksView(PermissionRequiredMixin, View):
    template_name = 'dashboard/form_one_ranks.html'
    form_class = ApplicationRankForm
    permission_required = (
        "dashboard.add_application",
        "dashboard.change_application",
        "dashboard.add_rank",
        "dashboard.change_rank",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        application = Application.objects.filter(id=application_id).first()
        ranks = Rank.objects.all()
        context = {"application": application, "ranks": ranks}
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, application_id):
        application_id = request.POST.get("application_id")
        application = get_object_or_404(Application, id=application_id)

        # Process Ranks
        ranks = request.POST.getlist("ranks")
        dates = request.POST.getlist("dates")
        application.ranks.exclude(id__in=ranks).delete()
        for rank, date in zip(ranks, dates):
            rank_obj = ApplicationRank.objects.get_or_create(
                application_id=application_id, rank_id=rank, date=date)[0]
            rank_obj.created_by = request.user
        return redirect("dashboard:application_form_one_upload",
                        application.id)


class NewApplicationFormOneUploadView(PermissionRequiredMixin, View):
    template_name = 'dashboard/form_one_upload.html'
    permission_required = (
        "dashboard.add_applicationdocument",
        "dashboard.change_application",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        document_types = ApplicationDocumentType.objects.all()
        context = {
            "application": application,
            "document_types": document_types,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, application_id):
        document_types = ApplicationDocumentType.objects.all()
        for document_type in document_types:
            files = request.FILES.getlist(document_type.codename)
            for file in files:
                doc = ApplicationDocument.objects.get_or_create(
                    name=document_type.name,
                    document_type=document_type,
                    file=file,
                    application_id=application_id)[0]
                doc.save()
        return redirect(request.META.get("HTTP_REFERER"))


class UploadSignatureView(PermissionRequiredMixin, View):
    permission_required = ("dashboard.change_application", )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        return redirect("dashboard:index")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        signature = request.FILES.get("signature")
        if signature:
            application.signature = signature
            application.save()
            messages.info(request, "Signature has been uploaded")
        else:
            messages.warning(request, "No signature uploaded")
        return redirect(request.META.get("HTTP_REFERER") or "dashboard:index")


class NewApplicationFormOneReviewView(PermissionRequiredMixin, View):
    template_name = 'dashboard/application_review_page.html'
    permission_required = (
        "dashboard.view_application",
        "dashboard.view_applicationrank",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        document_types = ApplicationDocumentType.objects.all()
        context = {
            "application": application,
            "document_types": document_types,
        }
        return render(request, self.template_name, context)


class MyApplicationsView(PermissionRequiredMixin, View):
    template_name = 'dashboard/my_applications.html'
    permission_required = "dashboard.view_application"

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        applications = Application.objects.all().order_by("-updated_at")
        context = {"applications": applications}
        return render(request, self.template_name, context)


class SubmittedApplicationsView(PermissionRequiredMixin, View):
    template_name = 'dashboard/submitted_applications.html'
    permission_required = "dashboard.can_review_application"

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        applications = Application.objects.exclude(
            status=ApplicationStatus.DRAFT.value).order_by("-updated_at")
        context = {"applications": applications}
        return render(request, self.template_name, context)


class SubmittedApplicationReviewView(PermissionRequiredMixin, View):
    template_name = 'dashboard/submitted_application_review_page.html'
    permission_required = "dashboard.can_review_application"

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        if application.status == ApplicationStatus.SUMITTED:
            application.status = ApplicationStatus.PROCESSING.value
            application.save()
        document_types = ApplicationDocumentType.objects.all()
        context = {
            "application": application,
            "document_types": document_types,
        }
        return render(request, self.template_name, context)


class DeleteApplicationView(PermissionRequiredMixin, View):
    permission_required = "dashboard.delete_application"

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return redirect("dashboard:index")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        application_id = request.POST.get("application_id")
        count = Application.objects.filter(id=application_id).delete()
        if count and count[0]:
            messages.success(request, "Application deleted.")
        else:
            messages.info(request, "Application not found.")
        return redirect(request.META.get("HTTP_REFERER") or "dashboard:index")


class ApplicationDetailsView(PermissionRequiredMixin, View):
    template_name = 'dashboard/application_details.html'
    permission_required = (
        "dashboard.view_application",
        "dashboard.view_document",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        context = {"application": application}
        return render(request, self.template_name, context)


class ApplicationSubmissionView(PermissionRequiredMixin, View):
    template_name = 'dashboard/application_details.html'
    permission_required = ("dashboard.view_application", )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        return redirect("dashboard:index")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, application_id):
        application_id = request.POST.get("application_id")
        application = get_object_or_404(Application, id=application_id)
        application.status = ApplicationStatus.SUMITTED.value
        application.save()
        messages.success(request,
                         "Application submitted sucessfully for review.")
        # Send sms
        Sms.objects.create(number=application.contact,
                           inititated_by=request.user,
                           subject=APPLICATION_SUBMISSION_SUBJECT,
                           message=APPLICATION_SUBMISSION_MESSAGE)
        return redirect("dashboard:index")


class ApplicationProcessedView(PermissionRequiredMixin, View):
    """Mark an application as approved and processed.
    """
    permission_required = (
        "dashboard.view_application",
        "dashboard.change_application",
        "dashboard.can_review_application",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, *args, **kwargs):
        return redirect("dashboard:index")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        application_id = request.POST.get("application_id")
        application = get_object_or_404(Application, id=application_id)
        application.status = ApplicationStatus.PROCESSED.value
        application.save()
        # Send sms
        Sms.objects.create(number=application.contact,
                           inititated_by=request.user,
                           subject=APPLICATION_SUBMISSION_SUBJECT,
                           message=APPLICATION_PROCESSED_MESSAGE)
        messages.success(request, "Successfully processed application.")
        return redirect("dashboard:submitted_applications")


class RequestApplicationChangesView(PermissionRequiredMixin, View):
    """Request changes to be made on applications. 
    This enables the regional offices to edit and application and resubmit the application.
    """
    permission_required = (
        "dashboard.view_application",
        "dashboard.can_review_application",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, *args, **kwargs):
        return redirect("dashboard:index")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        application_id = request.POST.get("application_id")
        requested_changes = request.POST.get("requested_changes")
        application = get_object_or_404(Application, id=application_id)
        application.status = ApplicationStatus.REQUESTED_CHANGES.value
        application.requested_changes = requested_changes
        application.updated_by = request.user
        application.full_clean()
        application.save()

        # Create a notification for the user.
        Notification.objects.create(
            to_user=application.created_by,
            url=reverse("dashboard:application_form_one") +
            f"?application_id={application.id}",
            subject=f"Appication ID: {application.id}",
            message=f"Change Required.\n{requested_changes}",
            from_user=request.user)

        Sms.objects.create(
            number=application.contact,
            inititated_by=request.user,
            subject="Application Changes Requested",
            message=
            f"Hello {application.created_by.get_name()},\nAction is required for application with ID: {application.id}. Kindly visit the dashboard for more info."
        )
        messages.success(request, "Request sent.")

        return redirect(request.META.get("HTTP_REFERER") or "dashboard:index")


class FormOneCompletinView(View):
    template_name = 'dashboard/form_one_completion.html'

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        context = {
            "application": application,
        }
        return render(request, self.template_name, context)


class ResendSMSView(View):
    template_name = 'dashboard/form_one_completion.html'

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return redirect("dashboard:index")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        sms_id = request.POST.get("sms_id")
        sms = request.user.initiated_sms.filter(id=sms_id).first()
        if not sms:
            messages.error(request, "SMS not found.")
            return redirect(request.META.get("HTTP_REFERER"))
        res = send_sms(sms.id)
        logger.info(res.response)
        messages.success(request, "SMS resent.")
        return redirect(request.META.get("HTTP_REFERER"))
        
