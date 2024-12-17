from rest_framework import permissions
from core.apps.accounts.choices import RoleChoice


class PositionPermission(permissions.BasePermission):

    def __init__(self) -> None: ...

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        if request.user.role in [
            RoleChoice.ADMIN,
            RoleChoice.SUPERUSER,
        ]:
            return True
        return False
