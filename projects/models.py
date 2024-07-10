from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from accounts.abstracts import TimeStampedModel, UniversalIdModel
from invoices.utils import generate_reference
from projects.abstracts import AbstractProjectModel

User = get_user_model()


class Project(UniversalIdModel, TimeStampedModel, AbstractProjectModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)
    reference = models.CharField(max_length=10, blank=True, null=True, unique=True)

    PROJECT_STATUS = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )
    status = models.CharField(max_length=100, choices=PROJECT_STATUS, default="pending")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["created_at", "status"]


@receiver(pre_save, sender=Project)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")


@receiver(pre_save, sender=Project)
def reference_pre_save(sender, instance, **kwargs) -> None:
    if instance.reference is None or instance.reference == "":
        instance.reference = generate_reference()
