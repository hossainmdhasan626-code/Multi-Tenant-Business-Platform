# ---Drf---
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# ---Serializer---
from accounts.serializers import UserSerializer

# ---Services---
from accounts.services.user_register_services import user_register_services

# ---Custom Services---
from common.permissions.IsOwner import IsOwner
from common.permissions.IsOwnerOrManager import IsOwnerOrManager
from common.permissions.IsTenantUser import IsTenantUser

# Create your views here.


# টেন্ট এর একাউন্ট খুলে ও টেন্ট মালিক এর একাউন্ট তৈরী করা।
class RegisterCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        data = user_register_services().owner_register_services(request=request)

        return Response(
            {
                "message": "অ্যাকাউন্ট তৈরি সফল হয়েছে!",
                "token": data["token"],
                "tenant": data["tenant"],
                "data": data["data"],
                "role": data["role"],
            },
            status=status.HTTP_201_CREATED,
        )


class ManagerRegisterCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwner]

    def post(self, request):
        data = user_register_services().manager_register_services(request=request)

        return Response(
            {
                "message": "অ্যাকাউন্ট তৈরি সফল হয়েছে!",
                "token": data["token"],
                "tenant": data["tenant"],
                "data": data["data"],
                "role": data["role"],
            },
            status=status.HTTP_201_CREATED,
        )


class SalesmanRegisterCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser, IsOwnerOrManager]

    def post(self, request):

        data = user_register_services().salesman_register_services(request=request)

        return Response(
            {
                "message": "অ্যাকাউন্ট তৈরি সফল হয়েছে!",
                "token": data["token"],
                "tenant": data["tenant"],
                "data": data["data"],
                "role": data["role"],
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "সফলভাবে লগআউট করা হয়েছে।"}, status=status.HTTP_200_OK
        )


class MeAPIVier(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)
        return Response(
            {"message": "আপনার টেন্ট এর ডাটা সফল ভাবে পাওয়া গিয়েছে।", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
