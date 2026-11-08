# ---DRF---
from rest_framework import serializers

# ---Model---
from subscriptions.models import SubscriptionPlan, TenantSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_date",
            "updated_date",
        ]


class TenantSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSubscription
        fields = "__all__"
        read_only_fields = [
            "id",
            "tenant",
            "status",
            "start_date",
            "end_date",
            "trial_ends_at",
            "price_snapshot",
            "auto_renew",
            "renewed_at",
            "canceled_at",
            "created_date",
            "updated_date",
        ]
