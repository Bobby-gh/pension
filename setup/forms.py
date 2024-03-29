from django import forms
from django.contrib.auth.models import Group

from accounts.models import User
from setup.models import ApplicationDocumentType, Rank, RetirementReason


class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        exclude = [
            "id",
        ]


class ApplicationDocumentTypeForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocumentType
        exclude = [
            "id",
            'codename',
            "created_at",
            "updated_at",
        ]


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'name',
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = [
            "id",
            'photo',
            'email',
            'gender',
            'password',
            'last_login',
            "created_at",
            "updated_at",
        ]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = [
            "id",
            'photo',
            'email',
            'password',
            "username",
            'gender',
            'last_login',
            "created_at",
            "updated_at",
        ]


class RetirementReasonForm(forms.ModelForm):
    class Meta:
        model = RetirementReason
        exclude = [
            "id",
        ]
