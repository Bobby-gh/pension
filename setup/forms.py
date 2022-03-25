from django import forms
from django.contrib.auth.models import Group

from setup.models import ApplicationDocumentType, Rank


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