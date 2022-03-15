from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("apply",
         views.NewApplicationFormOneView.as_view(),
         name="application_form_one"),
    path("apply/upload",
         views.NewApplicationFormOneUploadView.as_view(),
         name="application_form_one_upload"),
    path("previous-applications",
         views.PreviousApplicationsView.as_view(),
         name="previous_applications"),
    path("delete-application",
         views.DeleteApplicationView.as_view(),
         name="delete_application"),
    path("application-details/<int:application_id>",
         views.ApplicationDetailsView.as_view(),
         name="application_details"),
]
