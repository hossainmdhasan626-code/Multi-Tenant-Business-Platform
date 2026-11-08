# ---Drf---
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# ---Custom permission---
from common.permissions.IsOwner import IsOwner
from common.permissions.IsTenantUser import IsTenantUser

# ---Services---
from credits_system.services.all_credit import all_credit
from credits_system.services.CreditTransactionServices import CreditTransactionServices


# Create your views here.
class TenantCreditBalanceAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwner]

    def get(self, request):
        credit_all = all_credit(tenant=request.user.tenant)

        return Response(
            {"message": "টিন্যান্টের ক্রেডিট সফলভাবে পাওয়া গেছে।", "data": credit_all},
            status=status.HTTP_200_OK,
        )


class CreditTransactionAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwner]

    def get(self, request):

        credit_transaction = CreditTransactionServices().CreditTransaction(
            tenant=request.user.tenant
        )

        return Response(
            {
                "message": "ক্রেডিট এর ট্রানসাকশান টি সফল ভাবে পাওয়া গেছে।",
                "data": credit_transaction,
            },
            status=status.HTTP_200_OK,
        )


class CreditTransactionDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwner]

    def get(self, request, pk):

        credit_details = CreditTransactionServices().CreditTransactionDetails(
            tenant=request.user.tenant, id=pk
        )

        return Response(
            {
                "message": "নির্দিষ্ট ক্রেডিট এর ট্রানসাকশান টি সফল ভাবে পাওয়া গেছে।",
                "data": credit_details,
            },
            status=status.HTTP_200_OK,
        )
