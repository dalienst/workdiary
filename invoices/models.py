from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from accounts.abstracts import TimeStampedModel, UniversalIdModel
from clients.models import Client
from invoices.utils import generate_reference

User = get_user_model()


class Invoice(UniversalIdModel, TimeStampedModel):
    """
    An invoice to be sent out to request payment from clients
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="invoice")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoices")
    title = models.CharField(max_length=255)
    issue_date = models.DateField()
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True)
    reference = models.CharField(max_length=10, blank=True, null=True, unique=True)

    def update_total_amount(self):
        self.total_amount = sum(item.total_price for item in self.items.all())
        self.save()

    def __str__(self):
        return self.client.name

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ["-created_at"]


@receiver(pre_save, sender=Invoice)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.title}-{instance.id}")


@receiver(pre_save, sender=Invoice)
def reference_pre_save(sender, instance, **kwargs) -> None:
    if instance.reference is None or instance.reference == "":
        instance.reference = generate_reference()


class InvoiceItem(UniversalIdModel, TimeStampedModel):
    """
    An invoice item to be added to an invoice
    """

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invoice_item"
    )
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    item_slug = models.SlugField(max_length=255, blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
        if not self.item_slug:
            self.item_slug = slugify(f"{self.user.get_username()}-{self.id}")
            self.save(update_fields=["item_slug"])
        self.invoice.update_total_amount()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"
        ordering = ["-created_at"]
