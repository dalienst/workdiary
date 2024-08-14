from django.contrib.auth import get_user_model
from django.db import models

from accounts.abstracts import ReferenceSlugModel, TimeStampedModel, UniversalIdModel
from company.models import Company

User = get_user_model()


class Schedule(UniversalIdModel, TimeStampedModel, ReferenceSlugModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_schedules"
    )
    name = models.CharField(max_length=255)
    workdays = models.JSONField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"

    def __str__(self):
        return self.name
