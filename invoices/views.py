# ---Django---
import logging

# ---Drf---
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# ---Custom permission---
from common.permissions.IsTenantUser import IsTenantUser

# ---Services---
from invoices.services.create_invoice_services import create_invoice
from invoices.services.get_invoices_details import get_invoices_details
from invoices.services.invoice_filter import invoice_filter

# logger = logging.getLogger(__name__)


# Create your views here.
class InvoicesAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]

    # ফিল্টার করে ডাটা বের করে আনা।
    def get(self, request):

        # ফিল্টার করে ডাটা বের করে আনা।
        data = invoice_filter(request=request, view_instance=self)

        return Response(
            {"message": "ফিল্টার করা ডাটা পাওয়া গিয়েছে। ", "data": data},
            status=status.HTTP_200_OK,
        )

    def post(self, request):

        try:
            tenant = request.user.tenant
            products_data = request.data.get("products", [])
            discount = request.data.get("discount", 0)
            customer_id = request.data.get("customer_id")
            customer_data = request.data.get("customer_data")
            salesman = request.user

            data = create_invoice(
                tenant=tenant,
                products_data=products_data,
                salesman=salesman,
                discount=discount,
                customer_id=customer_id,
                customer_data=customer_data,
            )

            return Response(
                {"message": "ইনভিসিসটি সফল ভাবে তৈরি হয়েছে।", "data": data},
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            # সার্ভিসের যেকোনো ভ্যালিডেশন এরর ক্লায়েন্টকে সুন্দরভাবে ব্যাক করা (400 Bad Request)
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            # setting e kaj baki configaration
            # logging.exception("কিছু একটা ভুল হয়েছে, আবার চেষ্টা করুন")
            return Response(
                {"error": "কিছু একটা ভুল হয়েছে, আবার চেষ্টা করুন"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class InvoicesDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]

    def get(self, request, pk):

        data = get_invoices_details(tenant=request.user.tenant, pk=pk)

        return Response(
            {
                "message": "আপনার চাওয়া ইনভিসেসটি পাওয়া গিয়েছে। ",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
