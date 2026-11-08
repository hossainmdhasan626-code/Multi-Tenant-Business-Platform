# ---Django---
from django.db import models

# ---Custom reuable field---
from common.models import TimeStampedModel


# Create your models here.
class Product(TimeStampedModel):
    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="product"
    )
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=00)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=00)
    stock_quantity = models.PositiveIntegerField(default=0)
    active_status = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "sku"], name="unique_tenant_sku")
        ]
