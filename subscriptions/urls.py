# ---Django---
from django.urls import path

# ---APIView---
from subscriptions.views import SubscriptionPlanAPIView, TenantSubscriptionAPIView

urlpatterns = [
    path("", SubscriptionPlanAPIView.as_view(), name="subscription_plan"),
    path(
        "subscription/", TenantSubscriptionAPIView.as_view(), name="tenant-subscription"
    ),
]
