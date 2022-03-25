from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from setup.forms import ApplicationDocumentTypeForm, GroupForm, RankForm
from setup.models import ApplicationDocumentType, Rank
from setup.mxins import CreateUpdateMixin, DeletionMixin
from django.apps import apps
from django.conf import settings
from accounts.models import User


class IndexView(PermissionRequiredMixin, View):
    template_name = "setup/index.html"
    permission_required = ("setup.can_setup_system", )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        document_types = ApplicationDocumentType.objects.all()
        ranks = Rank.objects.all().order_by("order")
        roles = Group.objects.all()
        users = User.objects.all()

        context = {
            "document_types": document_types,
            "ranks": ranks,
            "roles": roles,
            "users": users,
        }
        return render(request, self.template_name, context)


class CreateUpdateRank(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "setup/edit_rank.html"
    form_class = RankForm
    object_id_field = "rank_id"
    model_class = Rank
    object_name = "rank"
    permission_required = (
        "setup.can_setup_system",
        "setup.add_rank",
        "setup.change_rank",
    )


class DeleteRank(PermissionRequiredMixin, DeletionMixin):
    object_id_field = "rank_id"
    model_class = Rank
    permission_required = (
        "setup.can_setup_system",
        "setup.delete_rank",
    )


class CreateUpdateApplicationDocumentType(PermissionRequiredMixin,
                                          CreateUpdateMixin):
    template_name = "setup/edit_application_document_type.html"
    form_class = ApplicationDocumentTypeForm
    object_id_field = "document_type_id"
    model_class = ApplicationDocumentType
    object_name = "document_type"
    permission_required = (
        "setup.can_setup_system",
        "setup.add_application_document_type",
        "setup.change_application_document_type",
    )


class DeleteApplicationDocumentType(PermissionRequiredMixin, DeletionMixin):
    object_id_field = "document_type_id"
    model_class = ApplicationDocumentType
    permission_required = (
        "setup.can_setup_system",
        "setup.delete_application_document_type",
    )


class CreateUpdateGroup(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "setup/edit_role.html"
    form_class = GroupForm
    object_id_field = "role_id"
    model_class = Group
    object_name = "role"
    permission_required = (
        "setup.can_setup_system",
        "auth.add_group",
        "auth.change_group",
    )


class DeleteGroup(PermissionRequiredMixin, DeletionMixin):
    object_id_field = "role_id"
    model_class = Group
    permission_required = (
        "setup.can_setup_system",
        "auth.delete_group",
    )

class RoleManagementView(PermissionRequiredMixin, View):
    template_name = "setup/role_management.html"
    permission_required = (
        "setup.setup.can_managemnt_roles",
        "setup.can_setup_system",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, role_id):
        role = get_object_or_404(Group, id=role_id)
        permissions = Permission.objects.filter()[:0]
        apps_list = [
            app.split(".")[0] for app in settings.INSTALLED_APPS
            if not 'django' in app
        ]
        models = []
        for app in apps_list:
            models.extend([
                model._meta.model_name
                for _, model in apps.all_models[app].items()
            ])
        permissions = Permission.objects.filter(
            content_type__app_label__in=apps_list,
            content_type__model__in=models)
        context = {
            "role": role,
            "permissions": permissions,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, role_id):
        role = get_object_or_404(Group, id=role_id)
        permissions_codes = request.POST.getlist("permissions")
        permissions = Permission.objects.filter(codename__in=permissions_codes)

        # Delete unchecked permissions
        role.permissions.exclude(codename__in=permissions_codes).delete()

        # Add permissions
        for permission in permissions:
            role.permissions.add(permission)
        return redirect(request.META.get("HTTP_REFERER") or "setup:dashboard")