from django.urls import path

from . import views

app_name = "setup"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("rank/change", views.CreateUpdateRank.as_view(), name="change_rank"),
    path("rank/delete", views.DeleteRank.as_view(), name="delete_rank"),
    path("document-type/change",
         views.CreateUpdateApplicationDocumentType.as_view(),
         name="change_document_type"),
    path("document-type/delete",
         views.DeleteApplicationDocumentType.as_view(),
         name="delete_document_type"),
    path("role/change", views.CreateUpdateGroup.as_view(), name="change_role"),
    path("role/delete", views.DeleteGroup.as_view(), name="delete_role"),
    path("user/delete", views.DeleteUser.as_view(), name="delete_user"),
    path("role/<int:role_id>/manage/",
         views.RoleManagementView.as_view(),
         name="manage_role"),
    path("user/change", views.CreateUpdateUser.as_view(), name="change_user"),
    path("retirement-reason/change",
         views.CreateUpdateRetirementReason.as_view(),
         name="change_retirement_reason"),
    path("retirement-reason/delete",
         views.DeleteRetirementReason.as_view(),
         name="delete_retirement_reason"),
    path("update-sysconfig",
         views.UpdateSysConfigView.as_view(),
         name="update_sysconfig"),
]