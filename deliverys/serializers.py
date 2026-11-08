# ---Drf---
from rest_framework import serializers

# ---Model---
from deliverys.models import CourierDelivery


class CourierDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierDelivery
        fields = "__all__"
        read_only_fields = [
            "tracking_id",
            "delivery_status",
            "booking_response",
            "shipped_at",
            "delivered_at",
            "returned_at",
        ]
