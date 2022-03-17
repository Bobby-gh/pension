from django import forms

from dashboard.models import Application, ApplicationRank


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
