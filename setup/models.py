from django.db import models


# Just for permissions
class SetupPerms(models.Model):
    class Meta:
        managed = False  # No database table creation or deletion  \
        # operations will be performed for this model.
        default_permissions = ()  # disable "add", "change", "delete"
        # and "view" default permissions
        permissions = (('can_setup_system', 'Can Setup System'),
                       ("can_managemnt_roles",
                        "Can Management role assignment user groups."))


class ApplicationDocumentType(models.Model):
    name = models.CharField(max_length=50)
    required = models.BooleanField(default=True)
    multiple = models.BooleanField(default=True)
    codename = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.codename:
            self.codename = "_".join(self.name.lower().split())
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Rank(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=20, default="")
    order = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.abbreviation:
            self.abbreviation = self.name[:3].upper()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class RetirementReason(models.Model):
    reason = models.TextField()
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.reason


class SysConfig(models.Model):
    sms_sender_id = models.CharField(max_length=100,
                                     unique=True,
                                     default="GHPOLPEN")
    send_sms = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
