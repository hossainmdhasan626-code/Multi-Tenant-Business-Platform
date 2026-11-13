# ---Drf---
from rest_framework.exceptions import NotFound

# ---Model---
from invoices.models import Invoice

# ---Serializer---
from invoices.serializers import InvoicesSerializer


def get_invoices_details(tenant, pk):

    try:
        data = Invoice.objects.prefetch_related("sale_items").get(tenant=tenant, id=pk)
    except Invoice.DoesNotExist:
        raise NotFound("ইনভয়েসটি ভেলিড নয়।")

    serializer = InvoicesSerializer(instance=data)

    return serializer.data
