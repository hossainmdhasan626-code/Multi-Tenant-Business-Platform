# ---Drf---
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# ---Custom permission---
from common.permissions.IsOwnerOrManager import IsOwnerOrManager
from common.permissions.IsTenantUser import IsTenantUser

# ---Services---
from dashboard.services.dashboard_services import dashboard_services


# Create your views here.
class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwnerOrManager]

    def get(self, request):

        dashboard_analytics = dashboard_services(tenant=request.user.tenant)

        return Response(
            {
                "message": "ড্যাশবোর্ড অ্যানালিটিক্স সফলভাবে লোড হয়েছে।",
                "data": dashboard_analytics,
            },
            status=status.HTTP_200_OK,
        )
