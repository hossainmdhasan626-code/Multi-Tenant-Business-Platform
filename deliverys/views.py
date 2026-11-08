# ---Drf---
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions.IsOwnerOrManager import IsOwnerOrManager

# ---Custom permission---
from common.permissions.IsTenantUser import IsTenantUser

# ---Services---
from deliverys.services.book_courier_delivery import book_courier_delivery


# Create your views here.
class CourierDeliveryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwnerOrManager]

    def post(self, request):

        invoice_id = request.data.get("invoice_id")

        if not invoice_id:
            return Response(
                {
                    "error": "ইনভয়েস আইডি প্রদান করা বাধ্যতামূলক।",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        book_courier = book_courier_delivery(
            invoice_id=invoice_id, tenant=request.user.tenant
        )

        return Response(
            {"message": "কুরিয়ার বুকিং সফলভাবে সম্পন্ন হয়েছে", "data": book_courier},
            status=status.HTTP_201_CREATED,
        )
