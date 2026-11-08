# ---Django---
from django.urls import reverse

# ---Drf---
from rest_framework import status
from rest_framework.test import APITestCase

# ---Model---
from accounts.models import User
from products.models import Product
from stock_movement.models import StockMovement
from tenants.models import Tenant


# Create your tests here.
class StockMovementAPITest(APITestCase):
    def setUp(self):

        self.tenant_1 = Tenant.objects.create(business_name="tenant_1", status=True)

        self.salesman = User.objects.create(role="SALESMAN", tenant=self.tenant_1)

        self.product_1 = Product.objects.create(
            tenant=self.tenant_1,
            name="product_1",
            sku="1",
            cost_price=700,
            selling_price=1000,
            stock_quantity=20,
        )

        self.stock_movement_1 = StockMovement.objects.create(
            id=1,
            tenant=self.tenant_1,
            product=self.product_1,
            quantity=5,
            movement_type="SALE",
            created_by=self.salesman,
        )

        self.stock_movement_url = reverse("stock-movement")
        self.stock_movement_detail_url = reverse(
            "stock_movement_details", kwargs={"pk": self.stock_movement_1.pk}
        )

    # স্টক মুভমেন্টস বের করে আনা।
    def test_stock_movement(self):

        self.client.force_authenticate(user=self.salesman)

        response = self.client.get(self.stock_movement_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["message"], "স্টক মুভমেন্ট গুলি সফল ভাবে পাওয়া গেছে।")

        self.assertEqual(StockMovement.objects.filter(tenant=self.tenant_1).count(), 1)

    # def test_stock_movement_details(self):

    #     self.client.force_authenticate(user=self.salesman)

    #     response = self.client.get(self.stock_movement_detail_url)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn("data", response.data)
    #     self.assertEqual(
    #         "নির্দিষ্ট স্টক মুভমেন্টটি সফল ভাবে পাওয়া গিয়েছে।", response.data["message"]
    #     )

    #     self.assertEqual(response.data["data"]["id"], self.stock_movement_1.pk)
