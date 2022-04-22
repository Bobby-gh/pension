from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from accounts.managers import AccountManager
from pension.utils.constants import REGIONS


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to="accounts", null=True, blank=True)
    surname = models.CharField(max_length=200, null=True, blank=True)
    other_names = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField()
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    region = models.CharField(max_length=50, choices=REGIONS)

    # Django stuff for authentication
    USERNAME_FIELD = "username"
    objects = AccountManager()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users"

    def get_title(self):
        if self.groups.filter(name__icontains="National"):
            return "Nat. Office"
        elif self.groups.filter(name__icontains="Regional"):
            return "Rg. Office"

    def get_name(self):
        if self.surname and self.other_names:
            return f"{self.surname} {self.other_names}"
        return self.username

    def count_notifications(self):
        return self.notifications.filter(read=False).count()

    def get_notifications(self):
        notifications = self.notifications.filter().order_by("-id")
        notifications.update(read=True)
        return notifications[:100]

    def __str__(self):
        return self.username
