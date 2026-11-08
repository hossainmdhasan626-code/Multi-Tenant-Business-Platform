# ---DRF---
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions.IsOwner import IsOwner

# ---Custom permission---
from common.permissions.IsTenantUser import IsTenantUser

# ---Services---
from subscriptions.services.get_all_subscription_plan import get_all_subscription_plan
from subscriptions.services.tenant_subscription_services import (
    tenant_subscription_services,
)


# Create your views here.
# সব সাবস্ক্রিপশন প্ল্যান বের করে আনা।
class SubscriptionPlanAPIView(APIView):
    permission_classes = [AllowAny]

    # সব সাবস্ক্রিপশন প্ল্যান বের করে আনা।
    def get(self, request):

        all_subscriptions = get_all_subscription_plan()

        return Response(
            {"message": "সফলভাবে সাবস্ক্রিপশন প্ল্যান পাওয়া গেছে।", "data": all_subscriptions},
            status=status.HTTP_200_OK,
        )


class TenantSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwner]

    def post(self, request):

        tenant_subscription = tenant_subscription_services(
            data=request.data, tenant=request.user.tenant
        )

        return Response(
            {
                "message": "আপনার নেয়া সুপস্ক্রিপশনটি সফল ভাবে চালু হয়েছে।",
                "data": tenant_subscription,
            },
            status=status.HTTP_201_CREATED,
        )
