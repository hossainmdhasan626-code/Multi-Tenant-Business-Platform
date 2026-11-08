# ---Django---
from django.db import transaction

# ---Drf---
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from accounts.models import User

# ---Serializer---
from accounts.serializers import UserSerializer

# ---services---
from credits_system.services.create_first_free_credit import create_first_free_credit

# ---Model---
from tenants.models import Tenant


class user_register_services:
    # টেন্ট এর একাউন্ট খুলে ও টেন্ট মালিক এর একাউন্ট তৈরী করা।
    @transaction.atomic
    def owner_register_services(self, request):
        # টেন্ট তৈরির জন্য বিসনেস নাম বের করে আনা।
        business_name = request.data.pop("business_name")

        if not business_name:
            raise serializers.ValidationError("একাউন্ট তৈরির জন্য টেন্ট নাম টি দোর কার।")

        tenant = Tenant.objects.create(business_name=business_name)

        # ইউসার রেজিস্ট্রেশন করা।
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(
            tenant=tenant, role="TENANT_OWNER", is_staff=True, is_active=True
        )

        # token creat kora
        token, _ = Token.objects.get_or_create(user=user)

        # ফ্রি ক্রেডিট তৈরি করা।
        free_credit = create_first_free_credit(tenant=tenant, salesman=user)

        return {
            "token": token.key,
            "tenant": tenant.business_name,
            "data": serializer.data,
            "role": "TENANT_OWNER",
            # "free_credit": free_credit,
        }

    @transaction.atomic
    def manager_register_services(self, request):

        username = request.data.get("username")
        tenant = request.user.tenant

        if not username:
            raise ValidationError("একাউন্ট তৈরির জন্য উসারনেম দোরকার।")

        exist_username = User.objects.filter(tenant=tenant, username=username)
        if exist_username:
            raise serializers.ValidationError(
                "এই নামটি আগেই ব্যবহৃত হয়েছে। অন্য একটি নাম দিন।"
            )

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(tenant=tenant, role="STORE_MANAGER")

        # token creat kora
        token, _ = Token.objects.get_or_create(user=user)

        return {
            "token": token.key,
            "tenant": tenant.business_name,
            "data": serializer.data,
            "role": "STORE_MANAGER",
        }

    @transaction.atomic
    def salesman_register_services(self, request):

        username = request.data.get("username")
        tenant = request.user.tenant

        if not username:
            raise serializers.ValidationError("একাউন্ট তৈরির জন্য উসারনেম দোরকার।")

        exist_username = User.objects.filter(tenant=tenant, username=username)
        if exist_username:
            raise serializers.ValidationError(
                "এই নামটি আগেই ব্যবহৃত হয়েছে। অন্য একটি নাম দিন।"
            )

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(tenant=tenant, role="SALESMAN")

        token, _ = Token.objects.get_or_create(user=user)

        return {
            "token": token.key,
            "tenant": tenant.business_name,
            "data": serializer.data,
            "role": "SALESMAN",
        }
