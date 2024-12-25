from django.utils.translation import gettext_lazy as _
from rest_framework import permissions

from ..choices import RoleChoice


class PsixologPermission(permissions.BasePermission):

    def __init__(self) -> None: ...

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        return request.user.role == RoleChoice.PSIXOLOG


class LawyerPermission(permissions.BasePermission):

    def __init__(self) -> None: ...

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        return request.user.role == RoleChoice.LAWYER


class BusinessPermission(permissions.BasePermission):

    def __init__(self) -> None: ...

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        return request.user.role == RoleChoice.BUSINESS


class IsModeratorPermission(permissions.BasePermission):
    message = _("You are not a moderator")

    def __init__(self) -> None: ...

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        return request.user.role in RoleChoice.moderator_roles()
