from django.db import models

from accounts.models import User
from pension.utils.constants import REGIONS, ApplicationStatus
from setup.models import ApplicationDocumentType, Rank


class Application(models.Model):
    APPLICATION_STATUSES = (
        (ApplicationStatus.DRAFT.value, ApplicationStatus.DRAFT.value),
        (ApplicationStatus.SUMITTED.value, ApplicationStatus.SUMITTED.value),
        (ApplicationStatus.REQUESTED_CHANGES.value,
         ApplicationStatus.REQUESTED_CHANGES.value),
        (ApplicationStatus.PROCESSING.value,
         ApplicationStatus.PROCESSING.value),
    )
    surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="uploads/applications",
                              null=True,
                              blank=True)
    signature = models.ImageField(upload_to="uploads/signature",
                                  null=True,
                                  blank=True)
    rank = models.CharField(max_length=50)
    requested_changes = models.TextField(null=True, blank=True)
    retiring_date = models.DateField()
    reason = models.TextField()
    bank_name = models.CharField(max_length=200)
    bank_account = models.CharField(max_length=50)
    last_station = models.CharField(max_length=100)
    region = models.CharField(max_length=50, choices=REGIONS)
    contact = models.CharField(max_length=20)
    contact_address = models.TextField()
    status = models.CharField(max_length=50,
                              default=ApplicationStatus.DRAFT.value,
                              choices=APPLICATION_STATUSES)
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
        permissions = (
            ("can_review_application", "Change status"),
            ("can_generate_letter", "Generate Award Letter from Application"),
        )

    def get_status(self):
        return self.status.replace("_", " ").title()

    def can_edit(self):
        return (self.status == ApplicationStatus.DRAFT.value
                or self.status == ApplicationStatus.REQUESTED_CHANGES.value)

    def get_name(self):
        return f"{self.surname} {self.other_names}"

    def get_current_rank(self):
        return self.ranks.all().order_by("date").last().rank

    def all_sorted_ranks(self):
        return self.ranks.all().order_by("date")

    def __str__(self) -> str:
        return f"{self.surname} {self.other_names}"


class ApplicationDocument(models.Model):
    name = models.CharField(max_length=100)
    document_type = models.ForeignKey(ApplicationDocumentType,
                                      related_name="documents",
                                      on_delete=models.PROTECT)
    file = models.ImageField(upload_to="uplodas/documents", null=True)
    application = models.ForeignKey(Application,
                                    related_name="documents",
                                    on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name


class ApplicationRank(models.Model):
    application = models.ForeignKey(Application,
                                    related_name="ranks",
                                    on_delete=models.CASCADE)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.rank.name


class Notification(models.Model):
    to_user = models.ForeignKey(User,
                                related_name="notifications",
                                on_delete=models.CASCADE)
    from_user = models.ForeignKey(User,
                                  related_name="created_notifications",
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL)
    message = models.TextField()
    url = models.URLField(blank=True, null=True)
    subject = models.CharField(max_length=200)
    slug = models.CharField(max_length=250, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = "_".join(self.subject.lower().split())
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.message