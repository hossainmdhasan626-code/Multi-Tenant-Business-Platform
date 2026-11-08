# ---Django---
from django.db import models

# ---Custom reuable field---
from common.models import TimeStampedModel


class SaleItem(TimeStampedModel):
    sale = models.ForeignKey(
        "invoices.Invoice", on_delete=models.CASCADE, related_name="sale_items"
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True,
        related_name="sale_items",
    )

    # প্রোডাক্টের নাম (স্ন্যাপশট - নাম চেঞ্জ হলেও পুরোনো ইনভয়েসে আগের নামই থাকবে)
    product_name = models.CharField(max_length=255)

    # ৪. পরিমাণ
    quantity = models.PositiveIntegerField(default=1)

    # ৫. Price Snapshots (খুবই গুরুত্বপূর্ণ)
    selling_price_snapshot = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="বিক্রির সময়কার বিক্রয়মূল্য"
    )

    cost_price_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text="বিক্রির সময়কার কেনাদাম (লাভ-ক্ষতি হিসেবের জন্য)",
    )

    # লাইন টোটাল (quantity * selling_price_snapshot)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
