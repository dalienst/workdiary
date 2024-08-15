from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from accounts.abstracts import ReferenceSlugModel, TimeStampedModel, UniversalIdModel
from schedules.models import Schedule

User = get_user_model()


class Timesheet(UniversalIdModel, TimeStampedModel, ReferenceSlugModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="employee_timesheets"
    )
    shift = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="shifts")
    date = models.DateField(default=timezone.now)
    checkin = models.DateTimeField(null=True, blank=True)
    checkout = models.DateTimeField(null=True, blank=True)
    total_hours = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    is_overtime = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        default="Regular",
    )
    overtime_hours = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    class Meta:
        verbose_name = "Timesheet"
        verbose_name_plural = "Timesheets"
        unique_together = ("user", "shift", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user} - {self.shift.reference} - {self.date} - {self.status} - {self.shift.company.name}"
