from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.abstracts import TimeStampedModel, UniversalIdModel
from company.utils import generate_company_reference, generate_company_slug

User = get_user_model()


class Company(UniversalIdModel, TimeStampedModel):
    """
    model for company or businesses
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company")
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    no_of_employees = models.CharField(max_length=255)
    field = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = CloudinaryField("company_logo", blank=True, null=True)
    employees = models.ManyToManyField(
        User, related_name="company_employees", blank=True
    )
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)
    reference = models.CharField(max_length=10, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]


@receiver(pre_save, sender=Company)
def slug_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_company_slug()


@receiver(pre_save, sender=Company)
def reference_pre_save(sender, instance, *args, **kwargs):
    if not instance.reference:
        instance.reference = generate_company_reference()
