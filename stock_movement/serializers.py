# ---DRF---
from rest_framework import serializers

# ---Model---
from stock_movement.models import StockMovement


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = "__all__"
        read_only_fields = [
            "id",
            "tenant",
            "product",
            "quantity",
            "movement_type",
            "reference",
            "created_by",
            "created_date",
            "updated_date",
        ]
