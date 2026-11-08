# ---Django---
from django.urls import path

# ---APIView---
from customers.views import (
    CustomerAPIView,
    CustomerCreateAPIView,
    CustomerDetailUpdateDeleteAPIView,
)

urlpatterns = [
    path("", CustomerAPIView.as_view(), name="customer-list"),
    path("create/", CustomerCreateAPIView.as_view(), name="customer-create"),
    path(
        "<int:pk>/",
        CustomerDetailUpdateDeleteAPIView.as_view(),
        name="customer-detail-update-delete",
    ),
]
