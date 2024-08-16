from django.contrib.auth import get_user_model
from django.db import models

from accounts.abstracts import ReferenceSlugModel, TimeStampedModel, UniversalIdModel
from schedules.models import Schedule

User = get_user_model()


class Payroll(TimeStampedModel, UniversalIdModel, ReferenceSlugModel):
    """
    1. Generate payroll
    2. Send email
    3. Save to database
    4. Relate to different employees and shifts
    5. Calculate total hours
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payrolls_generated"
    )
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payrolls"
    )
    start = models.DateField()
    end = models.DateField()
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="shift_payrolls"
    )
    regular_hours = models.DecimalField(max_digits=5, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)
    is_locked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Payroll"
        verbose_name_plural = "Payrolls"

    def __str__(self):
        return f"{self.reference}: {self.employee} - {self.start} to {self.end}"
