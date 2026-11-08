# ---Drf---
from rest_framework.permissions import BasePermission


class IsTenantUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.tenant
            and request.user.tenant.status
        )
