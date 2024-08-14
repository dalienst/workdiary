from django.contrib.auth import get_user_model
from django.db import models

from accounts.abstracts import TimeStampedModel, UniversalIdModel
from company.models import Company

User = get_user_model()


class Schedule(UniversalIdModel, TimeStampedModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="schedules"
    )
    name = models.CharField(max_length=255)
    workdays = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
