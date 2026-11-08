# ---Django---
from django.urls import path

# ---DRF---
from rest_framework.authtoken.views import obtain_auth_token

# ---views---
from accounts.views import (
    LogoutAPIView,
    ManagerRegisterCreateAPIView,
    MeAPIVier,
    RegisterCreateAPIView,
    SalesmanRegisterCreateAPIView,
)

urlpatterns = [
    path("register/", RegisterCreateAPIView.as_view(), name="register"),
    path(
        "register/manager/",
        ManagerRegisterCreateAPIView.as_view(),
        name="manager-register",
    ),
    path(
        "register/salesman/",
        SalesmanRegisterCreateAPIView.as_view(),
        name="salesman-register",
    ),
    path(
        "me/",
        MeAPIVier.as_view(),
        name="user-me",
    ),
    path("login/", obtain_auth_token, name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
