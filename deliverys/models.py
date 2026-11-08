# ---Django---
from django.db import models

# ---Custom reuable field---
from common.models import TimeStampedModel


class CourierDelivery(TimeStampedModel):
    class DeliveryStatus(models.TextChoices):
        PENDING = "PENDING", "Pending Booking"
        BOOKED = "BOOKED", "Booked / Consignment Created"
        IN_TRANSIT = "IN_TRANSIT", "In Transit / Shipped"
        DELIVERED = "DELIVERED", "Delivered to Customer"
        RETURNED = "RETURNED", "Returned to Merchant"
        CANCELLED = "CANCELLED", "Cancelled"

    sale = models.OneToOneField(
        "invoices.Invoice",
        on_delete=models.CASCADE,
        related_name="courier_delivery",
    )

    # কুরিয়ার সার্ভিস (Steadfast, Pathao, RedX etc.)
    courier_name = models.CharField(
        max_length=50, default="Steadfast", help_text="e.g., Steadfast, Pathao, RedX"
    )

    # ট্র্যাকিং আইডি (কুরিয়ার কোম্পানি থেকে পাওয়া Consignment ID / Tracking Code)
    tracking_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text="Courier Tracking Number / Consignment ID",
    )

    # ডেলিভারির বর্তমান অবস্থা
    delivery_status = models.CharField(
        max_length=20, choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING
    )

    # বুকিং রেসপন্স (API থেকে প্রাপ্ত কাঁচা তথ্য সেভ রাখার জন্য)
    booking_response = models.JSONField(
        null=True,
        blank=True,
        help_text="Full JSON response received from courier API after booking",
    )

    shipped_at = models.DateTimeField(
        null=True, blank=True, help_text="কবে কুরিয়ারে হ্যান্ডওভার করা হয়েছে"
    )
    delivered_at = models.DateTimeField(
        null=True, blank=True, help_text="কাস্টমার কবে মাল বুঝে পেয়েছে"
    )
    returned_at = models.DateTimeField(
        null=True, blank=True, help_text="কখন প্রোডাক্ট রিটার্ন হয়েছে"
    )
