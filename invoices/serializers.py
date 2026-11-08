# ---Drf---
from rest_framework import serializers

# ---Model---
from invoices.models import Invoice

# ---Serializer---
from sale_items.serializers import SaleItemSerializers


class InvoicesSerializer(serializers.ModelSerializer):
    sale_item = SaleItemSerializers(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "sequence",
            "tenant",
            "customer",
            "created_by",
            "subtotal",
            "discount",
            "total",
            "sale_item",
            "status",
            "delivery_status",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["id", "sequence", "tenant", "created_date", "updated_date"]
