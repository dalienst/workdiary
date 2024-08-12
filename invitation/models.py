from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.abstracts import TimeStampedModel, UniversalIdModel
from company.models import Company
from invitation.utils import generate_slug

User = get_user_model()


class Invitation(UniversalIdModel, TimeStampedModel):
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True, null=True, blank=True)
    expiry = models.DateTimeField(blank=True, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="invitations"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invitations_sent"
    )

    slug = models.SlugField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"


@receiver(pre_save, sender=Invitation)
def slug_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug()
