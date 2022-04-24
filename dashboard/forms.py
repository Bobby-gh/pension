from django import forms

from dashboard.models import (Application, ApplicationRank, OfficeParticulars,
                              PaidOpenVoteService)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = [
            "id",
            "status",
            "created_by",
            "updated_by",
        ]


class ApplicationRankForm(forms.ModelForm):
    class Meta:
        model = ApplicationRank
        exclude = [
            "id",
            'application',
            "created_by",
            "updated_by",
        ]


class OfficeParticularsForm(forms.ModelForm):
    class Meta:
        model = OfficeParticulars
        exclude = [
            "id",
        ]


class PaidOpenVoteServiceForm(forms.ModelForm):
    class Meta:
        model = PaidOpenVoteService
        exclude = [
            "id",
        ]