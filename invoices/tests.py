# ---Django---
from django.urls import reverse

# ---Drf---
from rest_framework import status
from rest_framework.test import APITestCase

# ---Model---
from accounts.models import User
from credits_system.models import TenantCreditBalance
from customers.models import Customer
from invoices.models import Invoice
from products.models import Product
from tenants.models import Tenant


# Create your tests here.
class InvoicesAPITest(APITestCase):
    def setUp(self):

        self.tenant_1 = Tenant.objects.create(business_name="tenant_1", status=True)
        self.tenant_2 = Tenant.objects.create(business_name="tenant_2", status=True)

        TenantCreditBalance.objects.create(
            tenant=self.tenant_1,
            free_credits=10,
            purchased_credits=0,
            is_unlimited=False,
        )

        self.product_1 = Product.objects.create(
            tenant=self.tenant_1,
            name="Wireless mouse",
            sku="1",
            cost_price=300,
            selling_price=500,
            stock_quantity=13,
        )

        self.product_2 = Product.objects.create(
            tenant=self.tenant_1,
            name="Computer monitor",
            sku="2",
            cost_price=30000,
            selling_price=50000,
            stock_quantity=19,
        )

        self.salesman = User.objects.create(
            role="SALESMAN",
            tenant=self.tenant_1,
            email="salesman@gmail.com",
            password="salesmanpassword",
        )

        self.customer_1 = Customer.objects.create(
            tenant=self.tenant_1,
            name="customer_1",
            phone="01236456978",
            active_status=True,
        )

        self.customer_2 = Customer.objects.create(
            tenant=self.tenant_1,
            name="customer_2",
            phone="01000000000",
            active_status=True,
        )

        self.invoice_1 = Invoice.objects.create(
            sequence=1,
            tenant=self.tenant_1,
            customer=self.customer_1,
            created_by=self.salesman,
            subtotal=1100,
            total=1100,
            status=Invoice.Status.UNPAID,
            delivery_status=Invoice.DeliveryStatus.PENDING,
        )

        self.invoice_2 = Invoice.objects.create(
            sequence=2,
            tenant=self.tenant_1,
            customer=self.customer_2,
            created_by=self.salesman,
            subtotal=14500,
            total=15000,
            status=Invoice.Status.PAID,
            delivery_status=Invoice.DeliveryStatus.PENDING,
        )

        self.invoices_url = reverse("invoices")

    def test_invoices_filter(self):

        self.client.force_authenticate(user=self.salesman)

        # স্টেটাস এর মাধ্যমে ফিল্টার চেক করা।
        filter_by_status_response = self.client.get(
            f"{self.invoices_url}?status=UNPAID"
        )
        self.assertEqual(filter_by_status_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(filter_by_status_response.data["data"]["results"]), 1)

        # কাস্টমার এর নাম আর নম্বর এর মাধ্যমে ফিল্টার চেক করা।
        filter_by_customer_response = self.client.get(
            f"{self.invoices_url}?customer=customer_1"
        )
        self.assertEqual(filter_by_customer_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(filter_by_customer_response.data["data"]["results"]), 1)

        filter_by_created_by_response = self.client.get(
            f"{self.invoices_url}?created_by=SALESMAN"
        )
        self.assertEqual(filter_by_created_by_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(filter_by_created_by_response.data["data"]["results"]), 2)

    # রেসপন্স এ যদি কাস্টমার এর  আইডি আসে।
    def test_invoices_created_by_customer_id(self):

        self.client.force_authenticate(user=self.salesman)

        payload = {
            "discount": 100,
            "customer_id": self.customer_1.id,
            "products": [
                {
                    "product_id": self.product_1.id,
                    "quantity": 3,
                },
                {
                    "product_id": self.product_2.id,
                    "quantity": 3,
                },
            ],
        }
        response = self.client.post(self.invoices_url, data=payload, format="json")

        if response.status_code == 500:
            print("\n=== 500 SERVER ERROR DETAILS ===")
            print(response.data)
            print("=================================\n")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.filter(tenant=self.tenant_1).count(), 3)
        self.assertIn(response.data["message"], "pukki")
        is_invoice_created = Invoice.objects.filter(
            tenant=self.tenant_1,
            customer__phone="01236456978",
            customer__name__icontains="customer_1",
        ).exists()
        self.assertTrue(is_invoice_created)

    # রেসপন্স এ যদি প্রথম বার আসে তাহলে কাস্টমার ডাটা নিয়ে ইন্ট্যান্স কাস্টমার একাউন্ট খেলে ইনভয়েস তৈরী করা ।
    def test_invoices_created_by_customer_data(self):

        self.client.force_authenticate(user=self.salesman)

        payload = {
            "customer_data": {"name": "Maria", "phone": "01536985214"},
            "products": [
                {
                    "product_id": self.product_1.id,
                    "quantity": 3,
                },
                {
                    "product_id": self.product_2.id,
                    "quantity": 3,
                },
            ],
        }

        response = self.client.post(self.invoices_url, data=payload, format="json")

        if response.status_code == 500:
            print("\n=== 500 SERVER ERROR DETAILS ===")
            print(response.data)
            print("=================================\n")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.filter(tenant=self.tenant_1).count(), 3)
        self.assertIn(response.data["message"], "pukki")
        is_invoice_created = Invoice.objects.filter(
            tenant=self.tenant_1,
            customer__phone="01536985214",
            customer__name__icontains="Maria",
        ).exists()
        self.assertTrue(is_invoice_created)

    # কাস্টমার যদি একাউন্ট খুলতে  সম্মতি না জানায় তাহলে ( "Walk in customer" "name" instance ) দিয়ে একাউন্ট  খুলা
    def test_invoices_for_walk_in_customer(self):

        self.client.force_authenticate(user=self.salesman)

        payload = {
            "products": [
                {
                    "product_id": self.product_1.id,
                    "quantity": 3,
                },
                {
                    "product_id": self.product_2.id,
                    "quantity": 3,
                },
            ],
        }

        response = self.client.post(self.invoices_url, data=payload, format="json")

        if response.status_code == 500:
            print("\n=== 500 SERVER ERROR DETAILS ===")
            print(response.data)
            print("=================================\n")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.filter(tenant=self.tenant_1).count(), 3)
        self.assertIn(response.data["message"], "pukki")
