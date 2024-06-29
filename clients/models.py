import random
import string

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from accounts.abstracts import TimeStampedModel, UniversalIdModel

User = get_user_model()


class Client(TimeStampedModel, UniversalIdModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients")
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)
    client_reference = models.CharField(
        max_length=10, blank=True, null=True, unique=True
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


@receiver(pre_save, sender=Client)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")


@receiver(pre_save, sender=Client)
def client_reference_pre_save(sender, instance, **kwargs) -> None:
    if instance.reference is None or instance.reference == "":
        instance.reference = generate_reference()


def generate_reference():
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choices(characters, k=8))
    return f"#{random_string}"
