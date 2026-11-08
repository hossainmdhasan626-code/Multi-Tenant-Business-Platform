# ---Django---
from django.urls import reverse

# ---Drf---
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

# ---Model---
from subscriptions.models import SubscriptionPlan
from tenants.models import Tenant


# Create your tests here.
class SubscriptionsPlansAPITest(APITestCase):
    def setUp(self):

        self.subscriptions_1 = SubscriptionPlan.objects.create(
            id=0,
            name="Classic Package",
            code=0,
            price=100,
            billing_cycle="MONTHLY",
            included_free_credits=500,
            is_unlimited_credits=False,
            max_users=5,
            max_products=1000,
            is_active=True,
        )

        self.subscriptions_2 = SubscriptionPlan.objects.create(
            id=1,
            name="Classi0c Student Package",
            code=1,
            price=200,
            billing_cycle="YEARLY",
            included_free_credits=1000,
            is_unlimited_credits=False,
            max_users=6,
            max_products=1200,
            is_active=False,
        )

        self.subscriptions_3 = SubscriptionPlan.objects.create(
            id=2,
            name="Classi0c Student Package",
            code=2,
            price=500,
            billing_cycle="YEARLY",
            included_free_credits=3000,
            is_unlimited_credits=False,
            max_users=15,
            max_products=10000,
            is_active=True,
        )

        self.tenant_1 = Tenant.objects.create(business_name="tenant_1", status=True)

        self.owner = User.objects.create(
            role=User.Role.TENANT_OWNER,
            tenant=self.tenant_1,
        )

        self.subscriptions_plans_urls = reverse("subscription_plan")
        self.tenant_subscription_urls = reverse("tenant-subscription")

    # সব সাবস্ক্রিপশন প্ল্যান বের করে আনা।
    def test_subscriptions_plans(self):

        response = self.client.get(self.subscriptions_plans_urls)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["message"], "সফলভাবে সাবস্ক্রিপশন প্ল্যান পাওয়া গেছে।")
        self.assertEqual(SubscriptionPlan.objects.all().count(), 3)
        self.assertEqual(len(response.data["data"]), 2)

    def test_tenant_subscription(self):

        self.client.force_authenticate(user=self.owner)

        payload = {
            "id": 0,
            "name": "Classic Package",
            "code": 0,
            "price": 100,
            "billing_cycle": "MONTHLY",
            "included_free_credits": 500,
            "is_unlimited_credits": False,
            "max_users": 5,
            "max_products": 1000,
            "is_active": True,
        }

        response = self.client.post(self.tenant_subscription_urls, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
