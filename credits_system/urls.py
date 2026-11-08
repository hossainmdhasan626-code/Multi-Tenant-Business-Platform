# ---Django---
from django.urls import path

# ---APIView---
from credits_system.views import (
    CreditTransactionAPIView,
    CreditTransactionDetailsAPIView,
    TenantCreditBalanceAPIView,
)

urlpatterns = [
    path("", TenantCreditBalanceAPIView.as_view(), name="tenant-credit-balance"),
    path(
        "credit-transaction/",
        CreditTransactionAPIView.as_view(),
        name="credit-transaction",
    ),
    path(
        "<int:pk>/credit-transaction-details/",
        CreditTransactionDetailsAPIView.as_view(),
        name="credit-transaction-details",
    ),
]
