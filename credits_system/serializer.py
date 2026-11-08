# ---DRF---
from rest_framework import serializers

# ---Model---
from credits_system.models import CreditTransaction, TenantCreditBalance


class TenantCreditBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantCreditBalance
        fields = "__all__"
        read_only_fields = [
            "id",
            "tenant",
        ]


class CreditTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditTransaction
        fields = "__all__"

        read_only_fields = [
            "id",
            "tenant",
            "amount",
            "transaction_type",
            "credit_bucket",
            "balance_after",
            "reference",
            "created_by",
            "created_date",
            "updated_date",
        ]
