# ---Django---
from django.urls import path

# ---APIView---
from customers.views import (
    CustomerAPIView,
    CustomerCreateAPIView,
    CustomerDetailUpdateAPIView,
)

urlpatterns = [
    path("", CustomerAPIView.as_view(), name="customer-list"),
    path("create/", CustomerCreateAPIView.as_view(), name="customer-create"),
    path(
        "<int:pk>/",
        CustomerDetailUpdateAPIView.as_view(),
        name="customer-detail-update-delete",
    ),
]
