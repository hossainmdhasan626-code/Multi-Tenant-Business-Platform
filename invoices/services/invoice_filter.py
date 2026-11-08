# ---Django---
from django.db.models import Q

# ---Custom pagination---
from common.services.reusable_custom_pagination import reusable_custom_pagination

# ---Model---
from invoices.models import Invoice

# ---Model---
from invoices.serializers import InvoicesSerializer


def invoice_filter(request, view_instance):

    invoice_data = Invoice.objects.filter(tenant=request.user.tenant)

    status = request.query_params.get("status")
    customer = request.query_params.get("customer")
    created_by = request.query_params.get("created_by")

    if status:
        invoice_data = invoice_data.filter(status=status)
    if customer:
        invoice_data = invoice_data.filter(
            Q(customer__name__icontains=customer)
            | Q(customer__phone__icontains=customer)
        )
    if created_by:
        invoice_data = invoice_data.filter(created_by__role__iexact=created_by)

    return reusable_custom_pagination(
        queryset=invoice_data,
        request=request,
        serializer_class=InvoicesSerializer,
        view_instance=view_instance,
        page_size=10,
    )
