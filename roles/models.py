from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.abstracts import TimeStampedModel, UniversalIdModel
from accounts.utils import generate_reference, generate_slug
from company.models import Company

User = get_user_model()


class Role(UniversalIdModel, TimeStampedModel):
    name = models.CharField(max_length=255)
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_rate = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=10, blank=True, null=True, unique=True)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="roles")
    employees = models.ManyToManyField(User, related_name="employee_roles", blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_roles"
    )

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Role)
def slug_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug()


@receiver(pre_save, sender=Role)
def reference_pre_save(sender, instance, *args, **kwargs):
    if not instance.reference:
        instance.reference = generate_reference()
