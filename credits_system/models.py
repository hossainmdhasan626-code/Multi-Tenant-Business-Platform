# ---Django---
from django.conf import settings
from django.db import models

# ---Custom reuable field---
from common.models import TimeStampedModel


# ১. টেন্যান্টের মূল ব্যালেন্স সামারি
class TenantCreditBalance(TimeStampedModel):
    tenant = models.OneToOneField(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="credit_balance",
    )
    free_credits = models.PositiveIntegerField(default=0)
    purchased_credits = models.PositiveIntegerField(default=0)
    is_unlimited = models.BooleanField(default=False)

    # পারফরম্যান্সের জন্য এই মাসের খরচ ট্র্যাক করে রাখা
    spent_this_month = models.PositiveIntegerField(default=0)


# ট্রানজেকশন হিস্ট্রি
class CreditTransaction(TimeStampedModel):
    class TransactionType(models.TextChoices):
        FREE_CREDIT = "FREE_CREDIT", "Free Monthly / Signup Credits"
        PURCHASE = "PURCHASE", "Direct Credit Top-up Purchase"
        SALE_DEDUCTION = "SALE_DEDUCTION", "Deduction per Invoice / Sale"
        REFUND = "REFUND", "Refunded Credits"
        SUBSCRIPTION_CONVERSION = (
            "SUBSCRIPTION_CONVERSION",
            "Converted via Plan Upgrade",
        )
        EXPIRED = "EXPIRED", "Monthly Free Credit Expired"

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="credit_transactions",
    )

    # ক্রেডিট কাটলে Negative (e.g. -1), ক্রেডিট যোগ হলে Positive (e.g. +100)
    amount = models.IntegerField()

    transaction_type = models.CharField(max_length=30, choices=TransactionType.choices)

    # কোন টাইপ ক্রেডিট থেকে কাটলো বা যোগ হলো
    credit_bucket = models.CharField(
        max_length=15,
        choices=[("FREE", "Free"), ("PURCHASED", "Purchased"), ("N/A", "N/A")],
        default="FREE",
    )

    # ট্রানজেকশনের সময়ের ব্যালেন্সের স্ন্যাপশট
    balance_after = models.PositiveIntegerField()

    reference = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="e.g., Invoice #1001 or Stripe Charge ID",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
