# ---Drf---
from rest_framework import serializers

# ---Model---
from sale_items.models import SaleItem


class SaleItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = [
            "id",
            "sale",
            "product",
            "product_name",
            "quantity",
            "selling_price_snapshot",
            "cost_price_snapshot",
            "line_total",
            "created_date",
            "updated_date",
        ]
        read_only_fields = [
            "id",
            "created_date",
            "updated_date",
        ]
