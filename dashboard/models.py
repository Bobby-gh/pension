from django.db import models

from accounts.models import User
from pension.utils.constants import REGIONS


class Application(models.Model):
    surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="applications", null=True, blank=True)
    rank = models.CharField(max_length=50)
    retiring_date = models.DateField()
    reason = models.TextField()
    bank_name = models.CharField(max_length=200)
    bank_account = models.CharField(max_length=50)
    last_station = models.CharField(max_length=100)
    region = models.CharField(max_length=50, choices=REGIONS)
    contact = models.CharField(max_length=20)
    contact_address = models.TextField()
    status = models.CharField(max_length=50)
    created_by = models.ForeignKey(User,
                                   related_name="created_applications",
                                   on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User,
                                   related_name="updated_applications",
                                   on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (("can_change_status", "Change status"), )

    def __str__(self) -> str:
        return f"{self.surname} {self.other_names}"


class Document(models.Model):
    name = models.CharField(max_length=100)
    application = models.ForeignKey(Application,
                                    related_name="documents",
                                    on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name
