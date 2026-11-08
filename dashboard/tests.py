# ---Django---
from django.urls import reverse

# ---Drf---
from rest_framework import status
from rest_framework.test import APITestCase

# ---Model---
from accounts.models import User
from customers.models import Customer
from invoices.models import Invoice
from products.models import Product
from sale_items.models import SaleItem
from tenants.models import Tenant


class DashboardAPITest(APITestCase):
    def setUp(self):
        # ১. টেন্যান্ট এবং ওনার ইউজার তৈরি
        self.tenant_1 = Tenant.objects.create(business_name="tenant_1", status=True)

        self.owner = User.objects.create(
            username="owner_user",
            role=User.Role.TENANT_OWNER,
            tenant=self.tenant_1,
            email="owner@gmail.com",
            password="ownerpassword",
        )

        # সাধারণ সেলসম্যান ইউজার (পারমিশন চেক করার জন্য)
        self.salesman = User.objects.create(
            username="salesman",
            role=User.Role.SALESMAN,
            tenant=self.tenant_1,
            email="salesman@gmail.com",
            password="salesmanpassword",
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

        self.customer_1 = Customer.objects.create(
            tenant=self.tenant_1,
            name="customer_1",
            phone="01236456978",
            active_status=True,
        )

        self.invoice_1 = Invoice.objects.create(
            tenant=self.tenant_1,
            customer=self.customer_1,
            created_by=self.salesman,
            subtotal=1100,
            total=1100,
            status=Invoice.Status.UNPAID,
            delivery_status=Invoice.DeliveryStatus.PENDING,
        )

        self.sale_item = SaleItem.objects.create(
            sale=self.invoice_1,
            product=self.product_1,
            product_name=self.product_1.name,
            quantity=self.product_1.stock_quantity,
            selling_price_snapshot=self.product_1.selling_price,
            cost_price_snapshot=self.product_1.cost_price,
            line_total=self.product_1.stock_quantity * self.product_1.selling_price,
        )

        # ড্যাশবোর্ড এপিআই ইউআরএল (আপনার urls.py অনুযায়ী নাম দিতে পারেন)
        self.dashboard_url = reverse("dashboard")

    def test_dashboard_access_by_owner(self):
        # ওনার হিসেবে লগইন বা অথেন্টিকেট করা
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(self.dashboard_url)

        # স্ট্যাটাস কোড এবং রেসপন্স স্ট্রাকচার যাচাই
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertIn("gross_revenue", response.data["data"])
        self.assertIn("net_profit", response.data["data"])
        self.assertIn("inventory_value", response.data["data"])

    def test_dashboard_access_denied_for_unauthorized_role(self):
        # সেলসম্যান হিসেবে লগইন করা (যাদের ড্যাশবোর্ড অ্যাক্সেস নেই)
        self.client.force_authenticate(user=self.salesman)

        response = self.client.get(self.dashboard_url)

        # এটি যেন ফোরবিডেন (403) বা আনঅথরাইজড রিটার্ন করে তা নিশ্চিত করা
        self.assertIn(
            response.status_code,
            [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED],
        )
