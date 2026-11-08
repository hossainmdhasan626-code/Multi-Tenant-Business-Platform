import uuid

# ----Django---
from django.db import transaction
from django.utils import timezone

# ---Drf---
from rest_framework.exceptions import ValidationError

# ---Model---
from deliverys.models import CourierDelivery

# ---Serializer---
from deliverys.serializers import CourierDeliverySerializer
from invoices.models import Invoice


@transaction.atomic
def book_courier_delivery(invoice_id, tenant, courier_name="Steadfast"):

    # ইনভয়েস বের করে আনা।
    try:
        invoice = Invoice.objects.get(tenant=tenant, id=invoice_id)
    except Invoice.DoesNotExist:
        raise ValidationError("নির্দিষ্ট ইনভয়েসটি পাওয়া যায়নি।")

    # রেন্ডম একটি ট্র্যাকিং আইডি
    unique_tracking_code = f"FAKE-{uuid.uuid4().hex[:8].upper()}"

    fake_api_response = {
        "status": "success",
        "message": "Consignment created successfully",
        "tracking_code": unique_tracking_code,
        "consignment": {
            "recipient_name": getattr(invoice, "customer_name", "Test Customer"),
            "recipient_phone": getattr(invoice.customer, "phone", "01700000000"),
            "recipient_address": getattr(
                invoice.customer, "address", "Dhaka, Bangladesh"
            ),
            "invoice": invoice.id,
            "amount_to_collect": float(getattr(invoice, "total_amount", 0.00)),
        },
    }

    courier_delivery = CourierDelivery.objects.create(
        sale=invoice,
        courier_name=courier_name,
        tracking_id=unique_tracking_code,
        delivery_status=CourierDelivery.DeliveryStatus.BOOKED,
        booking_response=fake_api_response,  # জেসন ফিল্ডে পুরো রেসপন্স সেভ হলো
        shipped_at=timezone.now(),
    )

    serializer = CourierDeliverySerializer(instance=courier_delivery)

    return serializer.data
