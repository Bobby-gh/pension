from django.urls import path

from . import ajax, views

app_name = "dashboard"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("notifications",
         views.NotificationsView.as_view(),
         name="notifications"),
    path("apply",
         views.NewApplicationFormOneView.as_view(),
         name="application_form_one"),
    path("apply/add-ranks/<int:application_id>",
         views.NewApplicationAddRanksView.as_view(),
         name="application_form_ranks"),
    path("apply/upload/<int:application_id>",
         views.NewApplicationFormOneUploadView.as_view(),
         name="application_form_one_upload"),
    path("apply/upload-signature/<int:application_id>",
         views.UploadSignatureView.as_view(),
         name="upload_signature"),
    path("apply/review/<int:application_id>",
         views.NewApplicationFormOneReviewView.as_view(),
         name="application_form_one_review"),
    path("my-applications",
         views.MyApplicationsView.as_view(),
         name="my_applications"),
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
    path("application-processed",
         views.ApplicationProcessedView.as_view(),
         name="application_processed"),
    path("request-changes",
         views.RequestApplicationChangesView.as_view(),
         name="request_changes"),
    path("<int:application_id>/complete-form-one",
         views.FormOneCompletinView.as_view(),
         name="complete_form_one"),
    path("resend-sms", views.ResendSMSView.as_view(), name="resend_sms"),
]

urlpatterns += [
    path("ajax/upload-photo",
         ajax.UploadPhotoView.as_view(),
         name="upload_photo"),
    path("ajax/delete-application-document",
         ajax.ApplicationDocumentDeletionView.as_view(),
         name="delete_application_ducument")
]
