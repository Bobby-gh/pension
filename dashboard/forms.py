from django import forms

from dashboard.models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = [
            "id",
            "status",
            "created_by",
            "updated_by",
        ]
