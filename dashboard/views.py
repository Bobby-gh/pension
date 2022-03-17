from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View

from dashboard.forms import ApplicationForm, ApplicationRankForm
from dashboard.models import Application, ApplicationRank, Rank
from pension.utils.constants import ApplicationStatus


class IndexView(View):
    template_name = 'dashboard/index.html'

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)


class NewApplicationFormOneView(PermissionRequiredMixin, View):
    template_name = 'dashboard/form_one.html'
    form_class = ApplicationForm
    permission_required = (
        "dashboard.add_application",
        "dashboard.change_application",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        application_id = request.GET.get("application_id")
        application = Application.objects.filter(id=application_id).first()
        context = {"application": application}
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        application_id = request.GET.get("application_id")
        application = Application.objects.filter(id=application_id).first()
        form = self.form_class(request.POST,
                               request.FILES or None,
                               instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.last_updated_by = request.user
            if not application_id:
                application.created_by = request.user
            application.status = ApplicationStatus.DRAFT.value
            application.save()
            messages.info(request, "Application has been saved")
            return redirect("dashboard:application_form_ranks", application.id)
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
        application = Application.objects.filter(id=application_id).first()

        # Process Ranks
        ranks = request.POST.getlist("ranks")
        dates = request.POST.getlist("dates")
        application.ranks.all().delete()
        for rank, date in zip(ranks, dates):
            rank_obj = ApplicationRank.objects.get_or_create(
                application_id=application_id, rank_id=rank, date=date)[0]
            rank_obj.created_by = request.user
        return redirect("dashboard:application_form_one_upload")


class NewApplicationFormOneUploadView(PermissionRequiredMixin, View):
    template_name = 'dashboard/form_one_upload.html'
    permission_required = (
        "dashboard.add_document",
        "dashboard.change_application",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)


class PreviousApplicationsView(PermissionRequiredMixin, View):
    template_name = 'dashboard/previous_applications.html'
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
        applications = Application.objects.filter(
            status=ApplicationStatus.SUMITTED.value).order_by("-updated_at")
        applications = Application.objects.all().order_by("-updated_at")
        context = {"applications": applications}
        return render(request, self.template_name, context)


class SubmittedApplicationReviewView(PermissionRequiredMixin, View):
    template_name = 'dashboard/submitted_application_review_page.html'
    permission_required = "dashboard.can_review_application"

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        context = {"application": application}
        return render(request, self.template_name, context)


class DeleteApplicationView(PermissionRequiredMixin, View):
    permission_required = "dashboard.delete_application"

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return redirect("dashboard:index")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        application_id = request.POST.get("application_id")
        count = [2] or Application.objects.filter(id=application_id).delete()
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
