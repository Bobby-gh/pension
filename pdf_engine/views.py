from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.models import Application

from .utils import render_to_pdf


class GenerateLetterView(PermissionRequiredMixin, View):
    template_name = 'pdf_engine/award_letter.html'
    permission_required = ("dashboard.can_generate_letter", )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        current_time = datetime.now().strftime("%d %B, %Y")
        context = {
            "application":
            application,
            "current_time":
            current_time,
            "ghana_police_logo_url":
            request.build_absolute_uri("/static/images/ghanapolice.png")
        }
        pdf = render_to_pdf(self.template_name, context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" % ("Award Letter")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found", status=404)


class GenerateControllerFormView(PermissionRequiredMixin, View):
    template_name = 'pdf_engine/controller_form.html'
    permission_required = [
        "dashboard.can_generate_letter",
        "dashboard.can_review_application",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, application_id):
        # application = get_object_or_404(Application, id=application_id)
        current_time = datetime.now().strftime("%d %B, %Y")
        context = {
            # "application":
            # application,
            "current_time":
            current_time,
            "ghana_police_logo_url":
            request.build_absolute_uri("/static/images/ghanapolice.png")
        }
        pdf = render_to_pdf(self.template_name, context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Controller_Form.pdf"
            content = f"inline; filename={filename}"
            download = request.GET.get("download")
            if download:
                content = f"attachment; filename={filename}"
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found", status=404)