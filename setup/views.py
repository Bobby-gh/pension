from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import User
from setup.forms import (ApplicationDocumentTypeForm, GroupForm, RankForm,
                         UserEditForm, UserForm)
from setup.models import ApplicationDocumentType, Rank
from setup.mxins import CreateUpdateMixin, DeletionMixin


class IndexView(PermissionRequiredMixin, View):
    template_name = "setup/index.html"
    permission_required = ("setup.can_setup_system", )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        document_types = ApplicationDocumentType.objects.all()
        ranks = Rank.objects.all().order_by("order")
        roles = Group.objects.all()
        users = User.objects.filter(is_superuser=False)

        context = {
            "document_types": document_types,
            "ranks": ranks,
            "roles": roles,
            "users": users,
            "user": None,
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
        "setup.add_applicationdocumenttype",
        "setup.change_applicationdocumenttype",
    )


class DeleteApplicationDocumentType(PermissionRequiredMixin, DeletionMixin):
    object_id_field = "document_type_id"
    model_class = ApplicationDocumentType
    permission_required = (
        "setup.can_setup_system",
        "setup.delete_applicationdocumenttype",
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


class DeleteUser(PermissionRequiredMixin, DeletionMixin):
    object_id_field = "user_id"
    model_class = User
    permission_required = (
        "setup.can_setup_system",
        "auth.delete_user",
    )


class RoleManagementView(PermissionRequiredMixin, View):
    template_name = "setup/role_management.html"
    permission_required = (
        "setup.can_managemnt_roles",
        "setup.can_setup_system",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, role_id):
        role = get_object_or_404(Group, id=role_id)
        permissions = Permission.objects.filter()[:0]
        apps_list = [app.split(".")[0] for app in settings.INSTALLED_APPS]
        models = []
        for app in apps_list:
            models.extend([
                model._meta.model_name
                for _, model in apps.all_models[app].items()
            ])
        permissions = Permission.objects.filter(
            content_type__app_label__in=apps_list,
            content_type__model__in=models)
        permissions = Permission.objects.all()
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
        role.permissions.set(permissions)
        return redirect(request.META.get("HTTP_REFERER") or "setup:dashboard")


class CreateUpdateUser(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "setup/edit_user.html"
    object_id_field = "user_id"
    form_class = UserForm
    edit_form_class = UserEditForm
    model_class = User
    object_name = "user"
    permission_required = (
        "setup.can_setup_system",
        "auth.add_user",
        "auth.change_user",
    )

    def get(self, request):
        object_id = request.GET.get(self.object_id_field)
        obj = get_object_or_404(self.model_class, id=object_id)
        roles = Group.objects.all()
        context = {
            self.object_name: obj,
            "roles": roles,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        user_id = request.POST.get("user_id") or None
        password = request.POST.get("password")
        username = request.POST.get("username")
        group_ids = request.POST.getlist("groups")
        conf_password = request.POST.get("conf_password")

        groups = Group.objects.filter(id__in=group_ids)

        if password and password != conf_password:
            messages.error(request, "Passwords do not match")
            return redirect(request.META.get("HTTP_REFERER") or "setup:index")

        user = User.objects.filter(
            id=user_id).first() or User.objects.create_user(username=username,
                                                            password=password)
        # Add to groups
        user.groups.set(groups)

        # Update fields
        for key, value in request.POST.items():
            if key in ["password", "username", "groups"]: continue
            if value and key and hasattr(user, key):
                setattr(user, key, value)
        if password: user.set_password(password)
        user.save()
        messages.success(request, "User updated successfully")
        return redirect("setup:index")
