# ---Django---
from django.conf import settings
from django.db import models

# ---Custom reuable field---
from common.models import TimeStampedModel


# Create your models here.
class StockMovement(TimeStampedModel):
    class MovementType(models.TextChoices):
        # DB VALU   DB VALUE     UI LABEL
        STOCK_IN = "STOCK_IN", "Stock Added (Purchase)"
        SALE = "SALE", "Sale (Invoice)"
        RETURN = "RETURN", "Customer Return"
        DAMAGE = "DAMAGE", "Damaged / Expired"
        ADJUSTMENT = "ADJUSTMENT", "Manual Adjustment"

    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="stock_movements"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="product_stock_movements",
    )
    quantity = models.IntegerField(
        help_text="+১০ হলে যোগ, -১০ হলে বিয়োগ"
    )  # যেমন: +50 বা -2
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)

    # কার মাধ্যমে বা কোন ডকুমেন্টের কারণে স্টক বদলাল (যেমন: Invoice #101)
    reference = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
