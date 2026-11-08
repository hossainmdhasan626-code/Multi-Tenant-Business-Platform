# ---Django---
from django.db.models import Q

# ---Custom pagination---
from common.services.reusable_custom_pagination import reusable_custom_pagination

# ---Model---
from customers.models import Customer

# ---Serializer---
from customers.serializer import CustomerSerializer


class CustomerServices:
    # কাস্টমার এর ডাটা বের(get) এবং সার্চ করে আনার জন্য।
    def get_customer(self, tenant, request, view_instance, search_query=None):

        customer_data = Customer.objects.filter(tenant=tenant)

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
    def customer_detail(self, tenant, id):

        customer_data = Customer.objects.filter(tenant=tenant, id=id).first()

        if not customer_data:
            return None
        serializ_data = CustomerSerializer(customer_data)
        return serializ_data.data

    def customer_update(self, request, tenant, customer_data, id):
        data = Customer.objects.filter(tenant=tenant, id=id).first()

        if not customer_data:
            return None

        serializ_data = CustomerSerializer(
            data, data=customer_data, context={"request": request}, partial=True
        )
        serializ_data.is_valid(raise_exception=True)
        serializ_data.save()
        return serializ_data.data

    def customer_delete(self, tenant, id):

        customer_data = Customer.objects.filter(tenant=tenant, id=id).first()

        if not customer_data:
            return False

        customer_data.delete()
        return True
