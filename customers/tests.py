# ---Django---
from django.urls import reverse

# ---Drf---
from rest_framework import status
from rest_framework.test import APITestCase

# ---Model---
from accounts.models import User
from customers.models import Customer
from tenants.models import Tenant


# Create your tests here.
class CustomerAPITest(APITestCase):
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

        # Salesman বানানো
        self.salesman_user = User.objects.create(
            username="salesman_username",
            role="SALESMAN",
            tenant=self.tenant_1,
            email="salesman@tenant1.com",
            password="salesman123",
        )

        self.customer_1 = Customer.objects.create(
            id=0, tenant=self.tenant_1, name="customer_1_hasan", active_status=True
        )
        self.customer_2 = Customer.objects.create(
            id=1, tenant=self.tenant_1, name="customer_2_mahim", active_status=True
        )

        self.customer_3 = Customer.objects.create(
            id=2, tenant=self.tenant_2, name="customer_3_mim", active_status=True
        )

        # Endpoints
        self.customer_url = reverse("customer-list")
        self.customer_create_url = reverse("customer-create")
        self.customer_detail_update_delete_url = reverse(
            "customer-detail-update-delete", kwargs={"pk": self.customer_1.pk}
        )

    # কাস্টমার এর ডাটা বের(get) এবং সার্চ করে আনার জন্য।
    def test_get_customer_data_and_get_customer_data_by_search(self):

        self.client.force_authenticate(user=self.owner_user)

        response = self.client.get(self.customer_url)

        # স্টেটাস চেক।
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # কি(key) চেক।
        self.assertIn("data", response.data)
        self.assertEqual(response.data["message"], "Customer retrieved successfully.")

        # Length চেক।
        self.assertEqual(len(response.data["data"]["results"]), 2)

        # ডাটাবেসে লেভেল এ চেক।
        is_customer_in_db = Customer.objects.filter(
            tenant=self.tenant_1, name__icontains="hasan"
        ).exists()
        self.assertTrue(
            is_customer_in_db, "Something is wrong with customer plese check"
        )

        # সার্চ
        search_response = self.client.get(f"{self.customer_url}?search=ma")

        # স্টেটাস চেক।
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)

        # কি(key) চেক।
        self.assertIn("data", search_response.data)
        self.assertEqual(
            search_response.data["message"], "Customer retrieved successfully."
        )

        # Length চেক।
        self.assertEqual(len(search_response.data["data"]["results"]), 1)

        # নেগেটিভ চেক।
        negative_test = Customer.objects.filter(
            tenant=self.owner_user.tenant, name__icontains="mim"
        ).exists()
        self.assertFalse(negative_test)

    # নতুন কাস্টমার তৈরী করা।
    def test_customer_create(self):
        self.client.force_authenticate(user=self.owner_user)

        payload = {"name": "customer_1_taniya", "active_status": True}

        response = self.client.post(
            self.customer_create_url, data=payload, format="json"
        )

        # স্টেটাস চেক।
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # কি(key) চেক।
        self.assertIn("data", response.data)
        self.assertEqual(response.data["message"], "Customer created successfully.")

        # Field চেক।
        self.assertEqual(response.data["data"]["name"], "customer_1_taniya")

        # ডাটাবেসে লেভেল এ চেক।
        is_customer_created_in_db = Customer.objects.filter(
            tenant=self.owner_user.tenant, name__icontains="taniya"
        ).exists()
        self.assertTrue(is_customer_created_in_db, "Customer wasn't created")

    # নির্দিষ্ট কাস্টমার এর ডাটা বের করে আনা।
    def test_customer_detais(self):
        self.client.force_authenticate(user=self.owner_user)

        response = self.client.get(self.customer_detail_update_delete_url)

        # স্টেটাস চেক।
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # কি(key) চেক।
        self.assertIn("data", response.data)
        self.assertEqual(response.data["message"], "Customer retrieved successfully.")

        # Field চেক।
        self.assertEqual(response.data["data"]["name"], "customer_1_hasan")

        # ডাটাবেস লেভেল এ চেক।
        is_customer_in_db = Customer.objects.filter(
            tenant=self.owner_user.tenant, id=response.data["data"]["id"]
        ).exists()
        self.assertTrue(is_customer_in_db, "Customer data wasn't in db")

    # নির্দিষ্ট কাস্টমার এর ডাটা update এর জন্য।
    def test_customer_update_by_id(self):
        self.client.force_authenticate(user=self.owner_user)

        payload = {"name": "customer_1_mahmud", "active_status": False}
        response = self.client.patch(
            self.customer_detail_update_delete_url, data=payload, format="json"
        )

        # স্টেটাস চেক।
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # কি(key) চেক।
        self.assertIn("data", response.data)
        self.assertEqual(response.data["message"], "Customer updated successfully.")

        # ফিল্ড লেভেল চেক। updated হলো কিনা।
        self.assertNotEqual(response.data["data"]["name"], "customer_1_hasan")

        # ডাটাবেস লেভেল চেক।
        is_it_update_in_db = Customer.objects.filter(
            tenant=self.owner_user.tenant, name__icontains="customer_1_mahmud"
        ).exists()
        self.assertTrue(is_it_update_in_db, "Customer was not updated in the database!")

    # Salesman কাস্টমার এর ডাটা update করতে পারবে না।
    def test_customer_update_by_salesman_forbidden(self):
        self.client.force_authenticate(user=self.salesman_user)

        payload = {"name": "customer_1_mahmud", "active_status": False}
        response = self.client.patch(
            self.customer_detail_update_delete_url, data=payload, format="json"
        )

        # স্টেটাস চেক।
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # ডাটাবেস লেভেল চেক।
        is_customer_update_in_db = Customer.objects.filter(
            tenant=self.salesman_user.tenant, name__icontains="customer_1_mahmud"
        ).exists()
        self.assertFalse(is_customer_update_in_db, "Customer was updated by a salesman")

    # নির্দিষ্ট কাস্টমার এর ডাটা delete এর জন্য।
    def test_customer_delete(self):

        self.client.force_authenticate(user=self.owner_user)

        response = self.client.delete(self.customer_detail_update_delete_url)

        # কি(key) লেভেল চেক।
        self.assertEqual(response.data["message"], "Deleted successfully.")

        # ডাটাবেস লেভেল চেক।
        is_product_delete_in_db = Customer.objects.filter(
            tenant=self.owner_user.tenant, id=self.customer_1.pk
        ).exists()
        self.assertFalse(
            is_product_delete_in_db,
            "Product deletion failed! The product still exists in the tenant's database.",
        )

    # Salesman কাস্টমার এর ডাটা delete করতে পারবে না।
    def test_customer_delete_forbidden(self):
        self.client.force_authenticate(user=self.salesman_user)

        response = self.client.delete(self.customer_detail_update_delete_url)

        # স্টেটাস চেক।
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # ডাটাবেস লেভেল চেক।
        is_customer_in_db = Customer.objects.filter(
            tenant=self.salesman_user.tenant, id=self.customer_1.pk
        ).exists()
        self.assertTrue(is_customer_in_db, "Customer was deleted by a salesman")
