# ---Drf---
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions.IsOwnerOrManager import IsOwnerOrManager

# ---Custom permission---
from common.permissions.IsTenantUser import IsTenantUser

# ---Services---
from stock_movement.services.StockMovementServices import StockMovementServices


# Create your views here.
class StockMovementAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwnerOrManager]

    def get(self, request):
        stock_movement = StockMovementServices().get_stock_movement(
            tenant=request.user.tenant, request=request, view_instance=self
        )
        return Response(
            {"message": "স্টক মুভমেন্ট গুলি সফল ভাবে পাওয়া গেছে।", "data": stock_movement},
            status=status.HTTP_200_OK,
        )


class StockMovementDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwnerOrManager]

    def get(self, request, pk):
        stock_movement = StockMovementServices().get_details_stock_movement(
            tenant=request.user.tenant, stock_movement_id=pk
        )

        return Response(
            {
                "message": "স্টক মুভমেন্টটি সফল ভাবে পাওয়া গিয়েছে।",
                "data": stock_movement,
            },
            status=status.HTTP_200_OK,
        )
