# ---Django---
from django.urls import reverse

# ---Drf---
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

# ---Model---
from credits_system.models import CreditTransaction, TenantCreditBalance
from tenants.models import Tenant


# Create your tests here.
class CreditsSystemAPITest(APITestCase):
    def setUp(self):

        self.tenant_1 = Tenant.objects.create(business_name="tenannt_1", status=True)

        self.salesman = User.objects.create(
            role="SALESMAN",
            tenant=self.tenant_1,
            email="salesman@gmail.com",
            password="salesmanpassword",
        )

        self.tenant_credit_balance = TenantCreditBalance.objects.create(
            tenant=self.tenant_1,
            free_credits=1000,
            purchased_credits=12,
            is_unlimited=False,
        )

        self.amount_of_transaction = 10

        after_transaction_balance = (
            self.tenant_credit_balance.free_credits - self.amount_of_transaction
        )

        self.credit_transaction = CreditTransaction.objects.create(
            id=1,
            tenant=self.tenant_1,
            amount=self.amount_of_transaction,
            transaction_type="FREE_CREDIT",
            credit_bucket="FREE",
            balance_after=after_transaction_balance,
        )

        self.credit_transaction_1 = CreditTransaction.objects.create(
            id=2,
            tenant=self.tenant_1,
            amount=self.amount_of_transaction,
            transaction_type="PURCHASE",
            credit_bucket="FREE",
            balance_after=after_transaction_balance,
        )

        self.tenant_credit_balance_url = reverse("tenant-credit-balance")
        self.credit_transaction_url = reverse("credit-transaction")
        self.credit_transaction_details_url = reverse(
            "credit-transaction-details", kwargs={"pk": self.credit_transaction.pk}
        )

    # সব ক্রেডিট বের করে আনা।
    def test_tenant_credit_balance(self):

        self.client.force_authenticate(user=self.salesman)

        response = self.client.get(self.tenant_credit_balance_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["message"], "টিন্যান্টের ক্রেডিট সফলভাবে পাওয়া গেছে।")
        data = response.data["data"]
        self.assertEqual(data["free_credits"], 1000)
        self.assertEqual(data["purchased_credits"], 12)

    # ক্রেডিট ট্রানসাকশান বের করে আনা।
    def test_credit_transaction(self):

        self.client.force_authenticate(user=self.salesman)

        response = self.client.get(self.credit_transaction_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(
            response.data["message"], "ক্রেডিট এর ট্রানসাকশান টি সফল ভাবে পাওয়া গেছে।"
        )
        is_exist_in_db = CreditTransaction.objects.filter(tenant=self.tenant_1).exists()
        self.assertTrue(is_exist_in_db)

    def test_credit_transaction_details(self):

        self.client.force_authenticate(user=self.salesman)

        response = self.client.get(self.credit_transaction_details_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(
            response.data["message"], "নির্দিষ্ট ক্রেডিট এর ট্রানসাকশান টি সফল ভাবে পাওয়া গেছে।"
        )
        self.assertEqual(
            CreditTransaction.objects.filter(tenant=self.tenant_1).count(), 2
        )

        credit = CreditTransaction.objects.get(
            tenant=self.tenant_1, id=response.data["data"]["id"]
        )
        self.assertEqual(credit.tenant, self.tenant_1)
        self.assertEqual(credit.amount, self.amount_of_transaction)
