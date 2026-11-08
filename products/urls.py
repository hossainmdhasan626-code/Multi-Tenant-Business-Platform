# ---Django---
from django.urls import path

# ---APIView---
from products.views import (
    ProductAPIView,
    ProductCreateAPIView,
    ProductDetailUpdateDeleteAPIView,
    ProductUpdateStockQuantity,
)

urlpatterns = [
    path("", ProductAPIView.as_view(), name="product-list"),
    path("create/", ProductCreateAPIView.as_view(), name="product-create"),
    path(
        "<int:pk>/",
        ProductDetailUpdateDeleteAPIView.as_view(),
        name="product-detail-update-delete",
    ),
    path(
        "stock-in/<int:pk>/",
        ProductUpdateStockQuantity.as_view(),
        name="stock-movement",
    ),
]
