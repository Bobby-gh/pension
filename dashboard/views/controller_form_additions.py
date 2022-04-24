import logging
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from dashboard.forms import OfficeParticularsForm, PaidOpenVoteServiceForm
from django.utils.html import strip_tags
from dashboard.models import (Application, NoPayLeave, OfficeParticulars,
                              PaidOpenVoteService,
                              PensionableEmolumentDrawnBeforeRetirement,
                              ServiceBreak)

logger = logging.getLogger("django")


class AddPensionableEmolumentDrawnBeforeRetirementView(PermissionRequiredMixin,
                                                       View):
    permission_required = "dashboard.can_review_application"

    def get(self, request, application_id):
        return redirect("dashboard:index")

    def post(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        emolument = request.POST.get("emolument")
        PensionableEmolumentDrawnBeforeRetirement.objects.create(
            controller_form=application.controller_form,
            from_date=from_date,
            to_date=to_date,
            emolument=emolument)
        return redirect(request.META.get("HTTP_REFERER"))


class DeletePensionableEmolumentView(PermissionRequiredMixin, View):
    permission_required = "dashboard.can_review_application"

    def get(self, request, pk):
        PensionableEmolumentDrawnBeforeRetirement.objects.filter(
            id=pk).delete()
        return redirect(request.META.get("HTTP_REFERER"))


class AddNoPayLeaveView(PermissionRequiredMixin, View):
    permission_required = "dashboard.can_review_application"

    def get(self, request, application_id):
        return redirect("dashboard:index")

    def post(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        NoPayLeave.objects.create(controller_form=application.controller_form,
                                  from_date=from_date,
                                  to_date=to_date)
        return redirect(request.META.get("HTTP_REFERER"))


class DeleteNoPayLeaveView(PermissionRequiredMixin, View):
    permission_required = "dashboard.can_review_application"

    def get(self, request, pk):
        NoPayLeave.objects.filter(id=pk).delete()
        return redirect(request.META.get("HTTP_REFERER"))


class AddServiceBreakView(PermissionRequiredMixin, View):
    permission_required = "dashboard.can_review_application"

    def get(self, request, application_id):
        return redirect("dashboard:index")

    def post(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        ServiceBreak.objects.create(
            controller_form=application.controller_form,
            from_date=from_date,
            to_date=to_date)
        return redirect(request.META.get("HTTP_REFERER"))


class DeletServiceBreakView(PermissionRequiredMixin, View):
    permission_required = "dashboard.can_review_application"

    def get(self, request, pk):
        ServiceBreak.objects.filter(id=pk).delete()
        return redirect(request.META.get("HTTP_REFERER"))


class AddOfficeParticularsView(PermissionRequiredMixin, View):
    permission_required = "dashboard.can_review_application"

    def get(self, request, application_id):
        return redirect("dashboard:index")

    def post(self, request, application_id):
        form = OfficeParticularsForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            logger.error(form.errors)
            field, error = list(form.errors.items())[0]
            messages.error(request,
                           f"{form.fields[field].label}: {strip_tags(error)}")
        return redirect(request.META.get("HTTP_REFERER"))


class DeleteOfficeParticularsView(PermissionRequiredMixin, View):
    permission_required = "dashboard.can_review_application"

    def get(self, request, pk):
        OfficeParticulars.objects.filter(id=pk).delete()
        messages.info(request, "Delete successful")
        return redirect(request.META.get("HTTP_REFERER"))


class AddPaidOpenVoteServiceView(PermissionRequiredMixin, View):
    permission_required = "dashboard.can_review_application"

    def get(self, request, application_id):
        return redirect("dashboard:index")

    def post(self, request, application_id):
        form = PaidOpenVoteServiceForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            logger.error(form.errors)
            field, error = list(form.errors.items())[0]
            messages.error(request,
                           f"{form.fields[field].label}: {strip_tags(error)}")
        return redirect(request.META.get("HTTP_REFERER"))


class DeletePaidOpenVoteServiceView(PermissionRequiredMixin, View):
    permission_required = "dashboard.can_review_application"

    def get(self, request, pk):
        PaidOpenVoteService.objects.filter(id=pk).delete()
        messages.info(request, "Delete successful")
        return redirect(request.META.get("HTTP_REFERER"))
