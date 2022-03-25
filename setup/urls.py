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
    path("role/<int:role_id>/manage/",
         views.RoleManagementView.as_view(),
         name="manage_role"),
]
