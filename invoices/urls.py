# ---Django---
from django.urls import path

# ---APIView---
from invoices.views import InvoicesAPIView, InvoicesDetailsAPIView

urlpatterns = [
    path("", InvoicesAPIView.as_view(), name="invoices"),
    path("<int:pk>/", InvoicesDetailsAPIView.as_view(), name="invoices-details"),
]
