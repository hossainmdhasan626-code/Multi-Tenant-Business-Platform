# ---Django---
from django.db.models import Count, IntegerField, Q, Sum
from django.db.models.functions import Coalesce

# ---Drf---
from rest_framework.exceptions import NotFound

# ---Custom pagination---
from common.services.reusable_custom_pagination import reusable_custom_pagination

# ---Model---
from customers.models import Customer

# ---Serializer---
from customers.serializer import CustomerSerializer

# ---Services---
from customers.services.total_order_count_and_lifetime_spending import (
    total_order_count_and_lifetime_spending,
)
from invoices.models import Invoice


class CustomerServices:
    # কাস্টমার এর ডাটা বের(get) এবং সার্চ করে আনার জন্য।
    def get_customer(self, tenant, request, view_instance, search_query=None):

        query_set = Customer.objects.filter(tenant=tenant)

        customer_data = total_order_count_and_lifetime_spending(query_set=query_set)

        if search_query:
            customer_data = customer_data.filter(
                Q(name__icontains=search_query) | Q(phone__icontains=search_query)
            )

        return reusable_custom_pagination(
            queryset=customer_data,
            request=request,
            serializer_class=CustomerSerializer,
            view_instance=view_instance,
            page_size=10,
        )

    # নতুন কাস্টমার তৈরী করা।
    def customer_create(self, request, tenant, customer_data):

        serializ_data = CustomerSerializer(
            data=customer_data, context={"request": request}
        )
        serializ_data.is_valid(raise_exception=True)
        serializ_data.save(tenant=tenant)
        return serializ_data.data

    # নির্দিষ্ট কাস্টমার এর ডাটা বের করে আনা।
    def customer_detail(self, request, tenant, id):

        query_set = Customer.objects.filter(tenant=tenant, id=id)

        customer_data = total_order_count_and_lifetime_spending(
            query_set=query_set
        ).first()

        if customer_data is None:
            raise NotFound("আপনার চাওয়া কাস্টমার পাওয়া যায়নি।")

        serializ_data = CustomerSerializer(
            instance=customer_data, context={"request": request}
        )
        return serializ_data.data

    def customer_update(self, request, tenant, customer_data, id):

        query_set = Customer.objects.filter(tenant=tenant, id=id)

        data = total_order_count_and_lifetime_spending(query_set=query_set).first()

        if data is None:
            raise NotFound("আপনার চাওয়া কাস্টমার পাওয়া যায়নি।")

        serializ_data = CustomerSerializer(
            instance=data,
            data=customer_data,
            context={"request": request},
            partial=True,
        )
        serializ_data.is_valid(raise_exception=True)
        serializ_data.save()
        return serializ_data.data

    def customer_delete(self, tenant, id):

        try:
            query_set = Customer.objects.get(tenant=tenant, id=id)
        except Customer.DoesNotExist:
            raise NotFound("আপনার চাওয়া কাস্টমার পাওয়া যায়নি।")

        query_set.delete()
        return True
