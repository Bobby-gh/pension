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
]
