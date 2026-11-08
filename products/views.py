# ----Drf---
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# ---Custom permission---
from common.permissions.IsOwner import IsOwner
from common.permissions.IsOwnerOrManager import IsOwnerOrManager
from common.permissions.IsTenantUser import IsTenantUser

# ---Services---
from products.services.ProductServics import ProductServics

# Create your views here.


# সব প্রোডাক্ট এর ডাটা বের করা ও সার্চ করে প্রোডাক্ট এর ডাটা বের করা।
class ProductAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]

    # সব প্রোডাক্ট এর ডাটা বের করা ও সার্চ করে প্রোডাক্ট এর ডাটা বের করা।
    def get(self, request):

        product_data = ProductServics().get_products(
            tenant=request.user.tenant,
            request=request,
            view_instance=self,
            search_query=request.query_params.get("search"),
        )

        return Response(
            {"message": "পণ্যগুলো সফলভাবে পুনরুদ্ধার করা হয়েছে।", "data": product_data},
            status=status.HTTP_200_OK,
        )


# নতুন প্রোডাক্ট তৈরী করা।
class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwnerOrManager]

    # নতুন প্রোডাক্ট তৈরী করা।
    def post(self, request):

        output_serializer = ProductServics().product_create(
            tenant=request.user.tenant,
            data=request.data,
            salesmen=request.user,
            request=request,
        )
        return Response(
            {
                "message": "পণ্যটি সফলভাবে তৈরি করা হয়েছে।",
                "data": output_serializer,
            },
            status=status.HTTP_201_CREATED,
        )


# নির্দিষ্ট প্রোডাক্ট এর ডাটা আপডেটেড করা ও নির্দিষ্ট প্রোডাক্ট ডিলিট করা।
class ProductDetailUpdateDeleteAPIView(APIView):
    # মেথড অনুযায়ী আলাদা পারমিশন সেট করা
    def get_permissions(self):

        if self.request.method == "GET":
            return [IsAuthenticated(), IsTenantUser()]

        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsTenantUser(), IsOwner()]

        return [IsAuthenticated(), IsTenantUser(), IsOwnerOrManager()]

    # নির্দিষ্ট প্রোডাক্ট এর ডাটা বের করা।
    def get(self, request, pk):

        product_data = ProductServics().get_products_details(
            request=request, tenant=request.user.tenant, product_id=pk
        )

        if not product_data:
            return Response(
                {"message": "পণ্যটি খুঁজে পাওয়া যায়নি।"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "message": "পণ্যের বিবরণ সফলভাবে সংগ্রহ করা হয়েছে।",
                "data": product_data,
            },
            status=status.HTTP_200_OK,
        )

    # নির্দিষ্ট প্রোডাক্ট এর ডাটা আপডেটেড করা।
    def patch(self, request, pk):

        updated_product_data = ProductServics().patch_updatese_single_product(
            request=request,
            tenant=request.user.tenant,
            product_id=pk,
            product_data=request.data,
        )

        return Response(
            {"message": "Product updated successfully.", "data": updated_product_data},
            status=status.HTTP_200_OK,
        )

    # প্রোডাক্ট ডিলিট করা।
    def delete(self, request, pk):

        product = ProductServics().get_delete_product(
            tenant=request.user.tenant, product_id=pk
        )

        return Response(
            {"message": "প্রোডাক্টটি সফলভাবে মুছে ফেলা হয়েছে।"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductUpdateStockQuantity(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwnerOrManager]

    def patch(self, request, pk):

        product_quantity = request.data.get("stock_quantity")
        update_type = request.data.get("type")

        update_stock_quantity = ProductServics().patch_product_stock(
            product_id=pk,
            tenant=request.user.tenant,
            salesmen=request.user,
            product_quantity=product_quantity,
            update_type=update_type,
        )

        return Response(
            {
                "message": "প্রোডাক্ট স্টক সফল ভাবে পরিবর্তন করা হয়েছে। ",
                "data": update_stock_quantity,
            }
        )
