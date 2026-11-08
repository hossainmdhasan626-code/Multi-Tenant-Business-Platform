# ---Django---
from django.contrib.auth import get_user_model
from django.urls import reverse

# ---Model---
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# ---Model---
from accounts.models import User
from tenants.models import Tenant

User = get_user_model()


# Create your tests here.
class AuthAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.me_url = reverse("user-me")

        self.user_1 = User.objects.create_user(
            username="user_1", password="user_1_password"
        )

    # রেজিস্ট্রেশন চেক।
    def test_user_registration(self):

        data = {
            "username": "testuser",
            "password": "StrongPassword123!",
            "business_name": "tenant_1",
        }

        response = self.client.post(self.register_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertIn("data", response.data)
        self.assertEqual("অ্যাকাউন্ট তৈরি সফল হয়েছে!", response.data["message"])
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Tenant.objects.count(), 1)

    # লগইন এন্ড অথেনটিএন্টিকেশন চেক।
    def test_user_login(self):
        self.client.force_authenticate(user=self.user_1)

        data = {"username": self.user_1.username, "password": "user_1_password"}
        response = self.client.post(self.login_url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    # লগআউট চেক।
    def test_user_logout(self):

        self.client.force_authenticate(user=self.user_1)
        token = Token.objects.create(user=self.user_1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user_1).exists())

    # user এর ডাটা আসছে কিনা।
    def test_me(self):

        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertIn("আপনার টেন্ট এর ডাটা সফল ভাবে পাওয়া গিয়েছে।", response.data["message"])
        self.assertEqual(response.data["data"]["username"], self.user_1.username)
