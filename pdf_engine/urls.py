from django.urls import path

from . import views

app_name = "pdf"

urlpatterns = [
    path("generate-letters/<int:application_id>/",
         views.GenerateLetterView.as_view(),
         name="generate_letter"),
    path("controller-form/<int:application_id>/",
         views.GenerateControllerFormView.as_view(),
         name="controller_form"),
    path("generate-passport-size-photo/<int:application_id>/",
         views.GeneratePassportSizePhotoView.as_view(),
         name="generate_passport_size_photo"),
    path("documents-print-out/<int:application_id>/",
         views.DocumentsPrintOutView.as_view(),
         name="documents_print_out"),
]
