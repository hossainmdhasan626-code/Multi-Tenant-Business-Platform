# ---Drf---
from rest_framework.permissions import BasePermission

# ---Model---
from accounts.models import User


class IsOwnerOrManager(BasePermission):
    def has_permission(self, request, view):

        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.role == User.Role.TENANT_OWNER
                or request.user.role == User.Role.STORE_MANAGER
            )
        )
