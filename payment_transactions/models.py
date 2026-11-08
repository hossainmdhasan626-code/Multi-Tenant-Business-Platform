# ---Django---
from django.db import models

# ---Custom reuable field---
from common.models import TimeStampedModel


class PaymentTransaction(TimeStampedModel):
    tenants = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="apyment_transaction"
    )

    class Provider(models.TextChoices):
        BKASH = "BKASH", "bKash"
        NAGAD = "NAGAD", "Nagad"
        SSLCOMMERZ = "SSLCOMMERZ", "SSLCommerz"
        STRIPE = "STRIPE", "Stripe"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    class Purpose(models.TextChoices):
        SUBSCRIPTION = "SUBSCRIPTION", "Subscription Plan Purchase"
        CREDIT_TOPUP = "CREDIT_TOPUP", "Credit Top-up Purchase"

    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="payment_transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_provider = models.CharField(max_length=20, choices=Provider.choices)
    transaction_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    payment_purpose = models.CharField(max_length=30, choices=Purpose.choices)
