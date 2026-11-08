# ---Django---
from django.urls import path

# ---APIView---
from stock_movement.views import StockMovementAPIView, StockMovementDetailsAPIView

urlpatterns = [
    path("", StockMovementAPIView.as_view(), name="stock-movement"),
    path(
        "<int:pk>/",
        StockMovementDetailsAPIView.as_view(),
        name="stock_movement_details",
    ),
]
