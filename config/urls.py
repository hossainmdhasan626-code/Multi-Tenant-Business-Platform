# ---Django---
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/products/", include("products.urls")),
    path("api/customers/", include("customers.urls")),
    path("api/invoices/", include("invoices.urls")),
    path("api/stock-movement/", include("stock_movement.urls")),
    path("api/balance/", include("credits_system.urls")),
    path("api/subscription/", include("subscriptions.urls")),
    path("api/delivery/", include("deliverys.urls")),
    path("api/dashboard/", include("dashboard.urls")),
]
