import base64
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.models import Application


class UploadPhotoView(PermissionRequiredMixin, View):
    permission_required = "dashboard.change_application"

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        image_data = request.POST.get('image_data_url')
        application_id = request.POST.get('application_id')
        image_format, imgstr = image_data.split(';base64,')
        ext = image_format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr))
        myfile = "photo-" + time.strftime("%Y%m%d-%H%M%S") + "." + ext

        # Save photo
        app = get_object_or_404(Application, id=application_id)
        app.photo.save(myfile, data)
        messages.success(request, "Photo updated successfully.")

        return JsonResponse({})