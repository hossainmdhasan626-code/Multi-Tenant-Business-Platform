# ---Django---
from django.conf import settings
from django.db import models

# ---Custom reuable field---
from common.models import TimeStampedModel


# Create your models here.
class Invoice(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        UNPAID = "UNPAID", "Unpaid"
        PARTIALLY_PAID = "PARTIALLY_PAID", "Partially Paid"
        PAID = "PAID", "Paid"
        CANCELLED = "CANCELLED", "Cancelled"

    class DeliveryStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        RETURNED = "RETURNED", "Returned"

    sequence = models.IntegerField(default=0)

    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="invoice"
    )
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        related_name="customer",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="salesman",
    )

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=00)
    discount = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=00)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.UNPAID
    )
    delivery_status = models.CharField(
        max_length=20, choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "sequence"], name="unique_sequence_per_tenant"
            )
        ]
