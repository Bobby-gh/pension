from django.db import models

from accounts.models import User
from pension.utils.constants import REGIONS, ApplicationStatus
from setup.models import ApplicationDocumentType, Rank, RetirementReason


class ControllerForm(models.Model):
    application = models.OneToOneField("Application",
                                       related_name="controller_form",
                                       on_delete=models.CASCADE)
    expatriate = models.CharField(default="",
                                  max_length=100,
                                  null=True,
                                  blank=True)
    office = models.CharField(default="",
                              max_length=100,
                              null=True,
                              blank=True)
    dob = models.DateField(null=True, blank=True)
    pensionable_emolument = models.CharField(default="",
                                             max_length=100,
                                             null=True,
                                             blank=True)
    salary = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 null=True,
                                 blank=True)
    expatriation_pay = models.DecimalField(max_digits=10,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
    other_pensionable_emolument = models.DecimalField(max_digits=10,
                                                      decimal_places=2,
                                                      null=True,
                                                      blank=True)
    total_emolument = models.DecimalField(max_digits=10,
                                          decimal_places=2,
                                          null=True,
                                          blank=True)
    additions_claimed = models.TextField(null=True, blank=True)
    retirement_cause = models.ForeignKey(RetirementReason,
                                         null=True,
                                         blank=True,
                                         on_delete=models.SET_NULL)
    pension_receipt_status = models.CharField(default="",
                                              max_length=100,
                                              null=True,
                                              blank=True)
    commencement_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    leave_withou_pay_from = models.DateField(null=True, blank=True)
    leave_withou_pay_to = models.DateField(null=True, blank=True)
    open_vote_date = models.DateTimeField(null=True, blank=True)
    condonation_authority = models.CharField(default="",
                                             max_length=100,
                                             null=True,
                                             blank=True)
    other_scheduled_work_detail = models.TextField(null=True, blank=True)
    form_5_pensionable_emoluments = models.DecimalField(max_digits=10,
                                                        decimal_places=2,
                                                        null=True,
                                                        blank=True)
    non_scheduled_work_detail = models.TextField(null=True, blank=True)
    officers_option = models.TextField(null=True, blank=True)
    pension_commencement_date = models.DateField(null=True, blank=True)

    def aggregate_pensionable_emolument(self):
        total_pensionable_emoluments = self.total_pensionable_emoluments_drawn_before_retirements.all(
        )
        return sum([item.emolument for item in total_pensionable_emoluments])

    def one_third_of_aggregate_pensionable_emolument(self):
        return round(self.aggregate_pensionable_emolument() / 3, 2)

    def service_duration_months(self):
        if self.termination_date and self.commencement_date:
            return (self.termination_date - self.commencement_date).days // 30
        return 0

    def service_duration_days(self):
        if self.termination_date and self.commencement_date:
            return (self.termination_date - self.commencement_date).days % 30
        return 0

    #(c) Leave without salary (para. 13):
    def no_pay_leave_total_months(self):
        no_pay_leaves = self.no_pay_leaves.all()
        days = sum([item.get_days() for item in no_pay_leaves])
        return sum([item.get_months() for item in no_pay_leaves]) + days // 30

    #(c) Leave without salary (para. 13):
    def no_pay_leave_total_days(self):
        no_pay_leaves = self.no_pay_leaves.all()
        return sum([item.get_days() for item in no_pay_leaves]) % 30

    # (d) Break in service (para. 14 (aa))
    def service_break_total_months(self):
        breaks = self.service_breaks.all()
        days = sum([item.get_days() for item in breaks])
        return sum([item.get_months() for item in breaks]) + days // 30

    # (d) Break in service (para. 14 (aa))
    def service_break_total_days(self):
        breaks = self.service_breaks.all()
        return sum([item.get_days() for item in breaks]) % 30

    def paid_open_vote_service_total_months(self):
        paid_open_vote_services = self.paid_open_vote_services.all()
        paid_open_vote_service_days = sum(
            [item.get_days() for item in paid_open_vote_services])
        return sum([item.get_months() for item in paid_open_vote_services
                    ]) + paid_open_vote_service_days // 30

    def paid_open_vote_service_total_days(self):
        paid_open_vote_services = self.paid_open_vote_services.all()
        paid_open_vote_service_days = sum(
            [item.get_days() for item in paid_open_vote_services])
        return paid_open_vote_service_days % 30

    # (e) One-third of open vote service (para. 14(c)): 0 10
    def third_open_vote_service_months(self):
        paid_open_vote_services = self.paid_open_vote_services.all()
        paid_open_vote_service_days = sum(
            [item.get_days() for item in paid_open_vote_services])
        third_open_vote_service_days = paid_open_vote_service_days // 3
        third_open_vote_service_months = sum([
            item.get_months() for item in paid_open_vote_services
        ]) + third_open_vote_service_days // 30  # Add days to months
        third_open_vote_service_months //= 3  # Divide by 3
        return third_open_vote_service_months

    # (e) One-third of open vote service (para. 14(c)): 0 10
    def third_open_vote_service_days(self):
        paid_open_vote_services = self.paid_open_vote_services.all()
        paid_open_vote_service_days = sum(
            [item.get_days() for item in paid_open_vote_services])
        third_open_vote_service_days = paid_open_vote_service_days // 3
        third_open_vote_service_months = sum([
            item.get_months() for item in paid_open_vote_services
        ]) + third_open_vote_service_days // 30  # Add days to months
        third_open_vote_service_months //= 3  # Divide by 3
        third_open_vote_service_days %= 30  # Remove months from days
        return third_open_vote_service_days

    # (f) Total of (b), (c), and (e) .
    def total_of_b_c_e_months(self):
        return 0 + self.no_pay_leave_total_months(
        ) + self.third_open_vote_service_months() + (
            self.no_pay_leave_total_days() +
            self.third_open_vote_service_days()) // 30

    def total_of_b_c_e_days(self):
        return (0 + self.no_pay_leave_total_days() +
                self.third_open_vote_service_days()) % 30


class PensionableEmolumentDrawnBeforeRetirement(models.Model):
    label = models.CharField(max_length=100, default="")
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    controller_form = models.ForeignKey(
        ControllerForm,
        on_delete=models.CASCADE,
        related_name="total_pensionable_emoluments_drawn_before_retirements")
    emolument = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    null=True,
                                    blank=True)


class NoPayLeave(models.Model):
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    controller_form = models.ForeignKey(ControllerForm,
                                        on_delete=models.CASCADE,
                                        related_name="no_pay_leaves")

    def get_months(self):
        return (self.to_date - self.from_date).days // 30

    def get_days(self):
        return (self.to_date - self.from_date).days % 30


class ServiceBreak(models.Model):
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    controller_form = models.ForeignKey(ControllerForm,
                                        on_delete=models.CASCADE,
                                        related_name="service_breaks")

    def get_months(self):
        return (self.to_date - self.from_date).days // 30

    def get_days(self):
        return (self.to_date - self.from_date).days % 30


class PaidOpenVoteService(models.Model):
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    controller_form = models.ForeignKey(ControllerForm,
                                        on_delete=models.CASCADE,
                                        related_name="paid_open_vote_services")

    def get_months(self):
        return (self.to_date - self.from_date).days // 30

    def get_days(self):
        return (self.to_date - self.from_date).days % 30


class OfficeParticulars(models.Model):
    title = models.CharField(max_length=200)
    if_pensionable = models.CharField("If Pensionable", max_length=200)
    commencement_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    emoluments = models.TextField()
    controller_form = models.ForeignKey(ControllerForm,
                                        verbose_name="Controller Form",
                                        on_delete=models.CASCADE,
                                        related_name="office_particulars")

    def __str__(self) -> str:
        return self.title


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
    rank = models.ForeignKey(Rank,
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL)
    requested_changes = models.TextField(null=True, blank=True)
    retiring_date = models.DateField()
    reason = models.ForeignKey(RetirementReason,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    bank_name = models.CharField(max_length=200)
    bank_account = models.CharField(max_length=50)
    last_station = models.CharField(max_length=100)
    region = models.CharField(max_length=50, choices=REGIONS)
    contact = models.CharField(max_length=10)
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
            ("can_review_application", "Change application status"),
            ("can_generate_letter", "Generate award letter from application"),
        )

    def get_status(self):
        return self.status.replace("_", " ").title()

    def can_edit(self):
        return (self.status == ApplicationStatus.DRAFT.value
                or self.status == ApplicationStatus.REQUESTED_CHANGES.value
                or self.status == ApplicationStatus.SUMITTED.value)

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
                                      null=True,
                                      blank=True,
                                      on_delete=models.SET_NULL)
    file = models.ImageField(upload_to="uploads/documents", null=True)
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


class Sms(models.Model):
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField()
    initiated_by = models.ForeignKey(User,
                                     related_name="initiated_sms",
                                     null=True,
                                     on_delete=models.SET_NULL)
    number = models.CharField(max_length=10)
    response = models.TextField()
    status_message = models.TextField(null=True, blank=True)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SMS"
        verbose_name_plural = "SMS's"

    def save(self, *args, **kwargs):
        if not self.subject:
            self.subject = self.message[:50]
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.message
