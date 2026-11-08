# ---Django---
from django.db.models import F, Sum

# ---Model---
from invoices.models import Invoice
from products.models import Product
from sale_items.models import SaleItem


def dashboard_services(tenant):

    # সব স্যাল বের করে আনা।
    all_sale = SaleItem.objects.filter(
        sale__tenant=tenant, sale__status=Invoice.Status.PAID
    )

    # সম্পূর্ণ ব্যবসার প্রোডাক্ট এর ডিটেইলস বের করে আনা।
    all_tenant_product = Product.objects.filter(tenant=tenant, active_status=True)

    # গ্রস রেভিনিউ এবং মোট বিক্রিত পণ্যের পরিমাণ
    sale_dict = all_sale.aggregate(total_unit_sold=Sum("quantity"))

    invoice_dict = Invoice.objects.filter(
        tenant=tenant, status=Invoice.Status.PAID
    ).aggregate(total_revenue=Sum("total"))

    # গ্রস রেভিনিউ
    gross_revenue = invoice_dict["total_revenue"] or 0
    # মোট বিক্রিত পণ্যের পরিমাণ
    unit_sold = sale_dict["total_unit_sold"] or 0

    # মোট ক্রয়মূল্য বের করা
    cost_dict = all_sale.annotate(
        sale_item_cost=F("quantity") * F("cost_price_snapshot")
    ).aggregate(total_item_cost=Sum("sale_item_cost"))
    # মোট ক্রয়মূল্য
    cost = cost_dict["total_item_cost"] or 0

    # মোট লাভ
    net_profit = gross_revenue - cost

    # ইনভেন্টরি ভ্যালু
    inventory_value_dict = all_tenant_product.annotate(
        inventory_value=F("cost_price") * F("stock_quantity")
    ).aggregate(total_inventory_value=Sum("inventory_value"))
    # ইনভেন্টরি ভ্যালু
    inventory_value = inventory_value_dict["total_inventory_value"] or 0

    return {
        "unit_sold": unit_sold,
        "gross_revenue": gross_revenue,
        "cost": cost,
        "net_profit": net_profit,
        "inventory_value": inventory_value,
    }
