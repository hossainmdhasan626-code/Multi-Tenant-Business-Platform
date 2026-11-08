# ---Django---
from django.urls import reverse

# ---Drf---
from rest_framework import status
from rest_framework.test import APITestCase

# ---Model---
from accounts.models import User
from customers.models import Customer
from deliverys.models import CourierDelivery
from invoices.models import Invoice
from tenants.models import Tenant


# Create your tests here.
class CourierDeliveryAPITest(APITestCase):
    def setUp(self):

        self.tenant_1 = Tenant.objects.create(business_name="tenant_1", status=True)

        self.customer_1 = Customer.objects.create(
            tenant=self.tenant_1,
            name="customer_1",
            phone="01236456978",
            active_status=True,
        )

        self.owner = User.objects.create(
            role=User.Role.TENANT_OWNER,
            tenant=self.tenant_1,
            email="salesman@gmail.com",
            password="salesmanpassword",
        )

        self.invoice_1 = Invoice.objects.create(
            tenant=self.tenant_1,
            customer=self.customer_1,
            created_by=self.owner,
            subtotal=1100,
            total=1100,
            status=Invoice.Status.UNPAID,
            delivery_status=Invoice.DeliveryStatus.PENDING,
        )

        self.courier_delivery_url = reverse("courier-delivery")

    def test_courier_delivery(self):

        self.client.force_authenticate(user=self.owner)

        data = {"invoice_id": self.invoice_1.id}

        response = self.client.post(self.courier_delivery_url, data=data)

        # if response.status_code == 400:
        #     print("====================")
        #     print(response.data)
        #     print("====================")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["message"], "কুরিয়ার বুকিং সফলভাবে সম্পন্ন হয়েছে")
        self.assertEqual(
            CourierDelivery.objects.filter(
                sale__tenant=self.tenant_1, id=response.data["data"]["id"]
            ).count(),
            1,
        )
