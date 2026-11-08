# ---Django---
from django.urls import reverse

# ---Drf---
from rest_framework import status
from rest_framework.test import APITestCase

# ---Model---
from accounts.models import User
from products.models import Product
from tenants.models import Tenant


# Create your tests here.
class ProductAPITest(APITestCase):
    def setUp(self):

        # Tenant
        self.tenant_1 = Tenant.objects.create(business_name="one", status=True)
        self.tenant_2 = Tenant.objects.create(business_name="two", status=True)

        # Owener বানানো
        self.owner_user = User.objects.create(
            username="owner_username",
            role="TENANT_OWNER",
            tenant=self.tenant_1,
            email="owner@tenant1.com",
            password="owner123",
        )

        # টেস্ট প্রোডাক্ট ডাটা product_1
        self.product_1 = Product.objects.create(
            id=0,
            tenant=self.tenant_1,
            name="Laptop Lenovo",
            sku="1",
            cost_price=50000,
            selling_price=55000,
            stock_quantity=10,
            active_status=True,
        )

        # টেস্ট প্রোডাক্ট ডাটা product_2
        self.product_2 = Product.objects.create(
            id=1,
            tenant=self.tenant_1,
            name="Wireless Mouse",
            sku="2",
            cost_price=1500,
            selling_price=1800,
            stock_quantity=10,
            active_status=True,
        )

        # টেস্ট প্রোডাক্ট ডাটা other_product_with_tenant_2
        self.other_product_with_tenant_2 = Product.objects.create(
            id=3,
            tenant=self.tenant_2,
            name="Tenant 2 Laptop Apple",
            sku="3",
            cost_price=150000,
            selling_price=180000,
            stock_quantity=10,
            active_status=True,
        )

        # Endpoints
        self.product_url = reverse("product-list")
        self.product_create_url = reverse("product-create")
        self.product_detail_updated_delete_url = reverse(
            "product-detail-update-delete", kwargs={"pk": self.product_1.pk}
        )

    # সব ডাটা বের করে আনা ও সার্চ এর মাধ্যমে বের ডাটা বের করে আনা।
    def test_product_get_and_product_get_by_search(self):

        # Forcefully অথেন্টিকেড করানো।
        self.client.force_authenticate(user=self.owner_user)

        # সব প্রোডাক্ট বের করে আনা।
        responce = self.client.get(self.product_url)

        # স্টেটাস চেক।
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

        # কি(key) চেক
        self.assertIn("data", responce.data)
        self.assertEqual(responce.data["message"], "Products retrieved successfully.")

        # রেস্পন্স এর lenght চেক।
        self.assertEqual(len(responce.data["data"]["results"]), 2)

        # ডাটাবেস লেভেল এ চেক।
        total_db_count_all = Product.objects.count()
        self.assertEqual(total_db_count_all, 3)

        tenant_1_db_count = Product.objects.filter(
            tenant=self.owner_user.tenant
        ).count()
        self.assertEqual(tenant_1_db_count, 2)

        # সার্চ করে ডাটা বের করে আনা।
        search_responce = self.client.get(f"{self.product_url}?search=Wireless")

        # স্টেটাস চেক।
        self.assertEqual(search_responce.status_code, status.HTTP_200_OK)

        # কি(key) চেক।
        self.assertIn("data", search_responce.data)
        self.assertEqual(
            search_responce.data["message"], "Products retrieved successfully."
        )

        # রেস্পন্স এর lenght চেক।
        self.assertEqual(len(search_responce.data["data"]["results"]), 1)

        # ডাটাবেসে লেভেল এ চেক।
        is_Wireless_in_db = Product.objects.filter(
            tenant=self.owner_user.tenant, name__icontains="Wireless"
        ).exists()
        self.assertTrue(is_Wireless_in_db, "Wireless")

        # নেগেটিভ সার্চ।
        search_responce_nagative_test = self.client.get(
            f"{self.product_url}?search=Apple"
        )

        # স্টেটাস চেক।
        self.assertEqual(search_responce_nagative_test.status_code, status.HTTP_200_OK)

        # রেস্পন্স এর lenght চেক।
        self.assertEqual(len(search_responce_nagative_test.data["data"]["results"]), 0)

        # ডাটাবেস লেভেল এ চেক।
        is_Apple_in_db = Product.objects.filter(
            tenant=self.owner_user.tenant,
            name__icontains="Apple",
        ).exists()
        self.assertFalse(is_Apple_in_db, "Apple")

    # নতুম প্রোডাক্ট তৈরী।
    def test_create_product(self):

        # Forcefully অথেন্টিকেড করানো।
        self.client.force_authenticate(user=self.owner_user)

        # মক ডাটা।
        payload = {
            "name": "RGB Mechanical Keyboard",
            "sku": "KB-101",
            "cost_price": "45.00",
            "selling_price": "60.00",
            "stock_quantity": 20,
        }

        responce = self.client.post(
            self.product_create_url, data=payload, format="json"
        )

        # স্টেটাস চেক।
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)

        # কি(key) চেক।
        self.assertIn("data", responce.data)
        self.assertEqual(responce.data["message"], "Product created successfully.")

        # ফিল্ড চেক।
        self.assertEqual(responce.data["data"]["name"], payload["name"])
        self.assertEqual(responce.data["data"]["sku"], payload["sku"])

        # ডাটাবেস লেভেল এ চেক।
        is_created_product_in_db = Product.objects.filter(
            tenant=self.owner_user.tenant,
            sku=payload["sku"],
        ).exists()
        self.assertTrue(is_created_product_in_db, "KB-101")
        self.assertEqual(
            Product.objects.filter(tenant=self.owner_user.tenant).count(), 3
        )

    # নির্দিষ্ট প্রোডাক্ট এর ডাটা বের করে আনা।
    def test_get_product_detail_by_pk(self):

        # Forcefully অথেন্টিকেড করানো।
        self.client.force_authenticate(user=self.owner_user)

        responce = self.client.get(self.product_detail_updated_delete_url)

        # স্টেটাস চেক।
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

        # কি চেক।
        self.assertIn("data", responce.data)
        self.assertEqual(
            responce.data["message"], "Product details retrieved successfully."
        )

        # ফিল্ড লেভেল চেক।
        self.assertEqual(responce.data["data"]["id"], self.product_1.pk)
        self.assertEqual(responce.data["data"]["name"], self.product_1.name)
        self.assertEqual(responce.data["data"]["sku"], self.product_1.sku)

        # ডাটাবেস লেভেল চেক।
        is_specific_product_in_db = Product.objects.filter(
            tenant=self.owner_user.tenant, id=responce.data["data"]["id"]
        ).exists()
        self.assertTrue(is_specific_product_in_db, 0)

    # নির্দিষ্ট প্রোডাক্ট আপডেটেড এর জন্য।
    def test_product_updated(self):

        # Forcefully অথেন্টিকেড করানো।
        self.client.force_authenticate(user=self.owner_user)

        payload = {
            "name": "Laptop Lenovo Updated",
            "sku": "1",
            "cost_price": "50000.00",
            "selling_price": "58000.00",
            "stock_quantity": 15,
            "active_status": True,
        }

        responce = self.client.patch(
            self.product_detail_updated_delete_url, data=payload, format="json"
        )

        # স্টেটাস চেক।
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

        # কি(key) চেক।
        self.assertIn("data", responce.data)
        self.assertEqual(responce.data["message"], "Product updated successfully.")

        # ফিল্ড লেভেল চেক। updated হলো কিনা।
        self.assertNotEqual(responce.data["data"]["name"], "Laptop Lenovo")
        self.assertNotEqual(responce.data["data"]["selling_price"], 55000)
        self.assertNotEqual(responce.data["data"]["stock_quantity"], 10)
        self.assertEqual(responce.data["data"]["name"], "Laptop Lenovo Updated")
        self.assertEqual(responce.data["data"]["selling_price"], "58000.00")
        self.assertEqual(responce.data["data"]["stock_quantity"], 15)

        # ডাটাবেস লেভেল চেক।
        is_it_updated_name_in_db = Product.objects.filter(
            tenant=self.owner_user.tenant, name__icontains=responce.data["data"]["name"]
        ).exists()
        is_it_updated_selling_price_in_db = Product.objects.filter(
            tenant=self.owner_user.tenant,
            selling_price__exact=responce.data["data"]["selling_price"],
        ).exists()
        is_it_updated_stock_quantity_in_db = Product.objects.filter(
            tenant=self.owner_user.tenant,
            stock_quantity__exact=responce.data["data"]["stock_quantity"],
        ).exists()
        self.assertTrue(
            is_it_updated_name_in_db, "Name was not updated in the database!"
        )
        self.assertTrue(
            is_it_updated_selling_price_in_db,
            "Selling price was not updated in the database!",
        )
        self.assertTrue(
            is_it_updated_stock_quantity_in_db,
            "Stock quantity was not updated in the database!",
        )

    # নির্দিষ্ট প্রোডাক্ট ডিলিট এর জন্য।
    def test_product_delete(self):

        # Forcefully অথেন্টিকেড করানো।
        self.client.force_authenticate(user=self.owner_user)

        responce = self.client.delete(self.product_detail_updated_delete_url)

        # স্টেটাস চেক।
        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)

        # কি(key) লেভেল চেক।
        self.assertEqual(responce.data["message"], "Deleted successfully.")

        # ডাটাবেস লেভেল চেক।
        is_product_delete_in_db = Product.objects.filter(
            tenant=self.owner_user.tenant, id=self.product_1.id
        ).exists()
        self.assertFalse(
            is_product_delete_in_db,
            "Product deletion failed! The product still exists in the tenant's database.",
        )
