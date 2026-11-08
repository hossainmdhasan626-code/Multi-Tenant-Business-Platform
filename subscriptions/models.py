# ---Django---
from django.db import models
from django.utils import timezone

# ---Custom reuable field---
from common.models import TimeStampedModel


class SubscriptionPlan(TimeStampedModel):
    class BillingCycle(models.TextChoices):
        MONTHLY = "MONTHLY", "Monthly"
        YEARLY = "YEARLY", "Yearly"
        LIFETIME = "LIFETIME", "Lifetime"

    name = models.CharField(max_length=100)
    code = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    billing_cycle = models.CharField(
        max_length=20,
        choices=BillingCycle.choices,
        default=BillingCycle.MONTHLY,
    )

    # প্ল্যানের সাথে ক্রেডিটের মেলবন্ধন
    included_free_credits = models.PositiveIntegerField(
        default=0, help_text="প্রতি মাসের ১ তারিখে যে ফ্রি ক্রেডিট দেওয়া হবে"
    )
    is_unlimited_credits = models.BooleanField(
        default=False, help_text="সত্যি হলে এই প্ল্যানে ক্রেডিট ট্র্যাকিং লাগবে না"
    )

    # ফিচার ফ্ল্যাগ (Feature Flags / Limits)
    max_users = models.PositiveIntegerField(
        default=2, help_text="কতজন স্টাফ লগইন করতে পারবে"
    )
    max_products = models.PositiveIntegerField(
        default=500, help_text="কতটি প্রোডাক্ট সেভ করতে পারবে"
    )

    is_active = models.BooleanField(default=True)


class TenantSubscription(TimeStampedModel):
    class Status(models.TextChoices):
        TRIALLING = "TRIALLING", "Trial"
        ACTIVE = "ACTIVE", "Active"
        PAST_DUE = (
            "PAST_DUE",
            "Past Due (Payment Failed)",
        )  # টাকা না দিলে গ্রেস পিরিয়ড
        CANCELED = "CANCELED", "Canceled"
        EXPIRED = "EXPIRED", "Expired"

    tenant = models.OneToOneField(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="tenant_subscriptions",
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.TRIALLING
    )

    # মেয়াদ সংক্রান্ত তারিখ
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(help_text="বর্তমান বিলিং সাইকেলের শেষ মেয়াদ")
    trial_ends_at = models.DateTimeField(null=True, blank=True)

    # প্রাইসিং স্ন্যাপশট (পরবর্তীতে প্ল্যানের দাম বাড়লেও বর্তমান টেন্যান্টের চুক্তি অনুযায়ী আসল দাম ধরে রাখা)
    price_snapshot = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="সাবস্ক্রিপশনের সময় চুক্তিকৃত মূল্য"
    )

    # রিনিউয়াল তথ্য (Renewal Information)
    auto_renew = models.BooleanField(
        default=True,
        help_text="মেয়াদ শেষে স্বয়ংক্রিয়ভাবে কার্ড/bKash থেকে কেটে অটো রিনিউ হবে কিনা",
    )
    renewed_at = models.DateTimeField(
        null=True, blank=True, help_text="সর্বশেষ যে তারিখে রিনিউ করা হয়েছিল"
    )
    canceled_at = models.DateTimeField(
        null=True, blank=True, help_text="কবে সাবস্ক্রিপশন ক্যানসেল করেছে"
    )
