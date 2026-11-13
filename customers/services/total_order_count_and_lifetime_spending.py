# ---Django---
from django.db.models import Count, IntegerField, Q, Sum
from django.db.models.functions import Coalesce

# ---Model---
from invoices.models import Invoice


def total_order_count_and_lifetime_spending(query_set):

    data = query_set.annotate(
        total_orders_count=Coalesce(
            Count("customer", filter=Q(customer__status=Invoice.Status.PAID)),
            0,
            output_field=IntegerField(),
        ),
        lifetime_spending=Coalesce(
            Sum(
                "customer__total",
                filter=Q(customer__status=Invoice.Status.PAID),
            ),
            0,
            output_field=IntegerField(),
        ),
    )

    return data
