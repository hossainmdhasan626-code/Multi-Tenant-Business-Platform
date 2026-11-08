# ---Django---
from django.urls import path

# ---APIView---
from dashboard.views import DashboardAPIView

urlpatterns = [
    path("", DashboardAPIView.as_view(), name="dashboard"),
]
