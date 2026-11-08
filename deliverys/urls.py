# ---Django---
from django.urls import path

# ---APIView---
from deliverys.views import CourierDeliveryAPIView

urlpatterns = [
    path("", CourierDeliveryAPIView.as_view(), name="courier-delivery"),
]
