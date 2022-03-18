from django.urls import path

from . import ajax, views

app_name = "dashboard"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("apply",
         views.NewApplicationFormOneView.as_view(),
         name="application_form_one"),
    path("apply/add-ranks/<int:application_id>",
         views.NewApplicationAddRanksView.as_view(),
         name="application_form_ranks"),
    path("apply/upload/<int:application_id>",
         views.NewApplicationFormOneUploadView.as_view(),
         name="application_form_one_upload"),
    path("apply/review/<int:application_id>",
         views.NewApplicationFormOneReviewView.as_view(),
         name="application_form_one_review"),
    path("previous-applications",
         views.PreviousApplicationsView.as_view(),
         name="previous_applications"),
    path("submitted-applications",
         views.SubmittedApplicationsView.as_view(),
         name="submitted_applications"),
    path("submitted-application-review/<int:application_id>",
         views.SubmittedApplicationReviewView.as_view(),
         name="submitted_application_review"),
    path("delete-application",
         views.DeleteApplicationView.as_view(),
         name="delete_application"),
    path("application-details/<int:application_id>",
         views.ApplicationDetailsView.as_view(),
         name="application_details"),
    path("application-submission/<int:application_id>",
         views.ApplicationSubmissionView.as_view(),
         name="application_submission"),
]

urlpatterns += [
    path("ajax/upload-photo",
         ajax.UploadPhotoView.as_view(),
         name="upload_photo")
]
