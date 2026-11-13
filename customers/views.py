# ---Drf---
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# ---Custom permission---
from common.permissions.IsOwnerOrManager import IsOwnerOrManager
from common.permissions.IsTenantUser import IsTenantUser

# ---Servics---
from customers.services.CustomerServices import CustomerServices


# Create your views here.
# কাস্টমার এর ডাটা বের(get) এবং সার্চ করে আনার জন্য।
class CustomerAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]

    # কাস্টমার এর ডাটা বের(get) এবং সার্চ করে আনার জন্য।
    def get(self, request):

        customer_data = CustomerServices().get_customer(
            tenant=request.user.tenant,
            request=request,
            view_instance=self,
            search_query=request.query_params.get("search"),
        )
        return Response(
            {"message": "Customer retrieved successfully.", "data": customer_data},
            status=status.HTTP_200_OK,
        )


# নতুন কাস্টমার তৈরী করা।
class CustomerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]

    # নতুন কাস্টমার তৈরী করা।
    def post(self, request):

        customer_data = CustomerServices().customer_create(
            tenant=request.user.tenant, request=request, customer_data=request.data
        )
        return Response(
            {"message": "Customer created successfully.", "data": customer_data},
            status=status.HTTP_201_CREATED,
        )


class CustomerDetailUpdateDeleteAPIView(APIView):
    def get_permissions(self):

        if self.request.method == "GET":
            return [IsAuthenticated(), IsTenantUser()]

        return [IsAuthenticated(), IsTenantUser(), IsOwnerOrManager()]

    # নির্দিষ্ট কাস্টমার এর ডাটা বের করে আনা।
    def get(self, request, pk):

        customer_data = CustomerServices().customer_detail(
            request=request, tenant=request.user.tenant, id=pk
        )

        return Response(
            {"message": "Customer retrieved successfully.", "data": customer_data},
            status=status.HTTP_200_OK,
        )

    # নির্দিষ্ট কাস্টমার এর ডাটা update এর জন্য।
    def patch(self, request, pk):

        customer_data = CustomerServices().customer_update(
            request=request,
            tenant=request.user.tenant,
            customer_data=request.data,
            id=pk,
        )

        if customer_data is None:
            return Response(
                {"message": "Customer not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"message": "Customer updated successfully.", "data": customer_data},
            status=status.HTTP_200_OK,
        )

    # নির্দিষ্ট কাস্টমার এর ডাটা delete এর জন্য।
    def delete(self, request, pk):

        customer_data = CustomerServices().customer_delete(
            tenant=request.user.tenant, id=pk
        )

        if not customer_data:
            return Response(
                {"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
