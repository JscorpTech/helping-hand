from typing import Any

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError

from core.apps.accounts.choices import RoleChoice

from ..filters import ModeratorFilter
from ..serializers.chat import ListUserSerializer


@extend_schema(tags=["moderator"])
class ModeratorView(BaseViewSetMixin, GenericViewSet):

    def get_serializer_class(self) -> Any:
        match self.action:
            case "retrieve" | "list":
                return ListUserSerializer
            case _:
                return ListUserSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="role",
                type=str,
                description="Filter by role",
                required=False,
                enum=[RoleChoice.LAWYER, RoleChoice.PSIXOLOG],
            ),
        ],
    )
    @method_decorator(cache_page(60))
    def list(self, request):
        users = get_user_model().objects.filter(
            role__in=[
                RoleChoice.PSIXOLOG,
                RoleChoice.LAWYER,
            ]
        )
        django_filter = ModeratorFilter(request.GET, queryset=users)
        if not django_filter.is_valid():
            raise ValidationError({"detail": django_filter.errors})
        return Response(self.get_serializer(django_filter.qs, many=True).data)

    @method_decorator(cache_page(60))
    def retrieve(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        if user.role in [RoleChoice.USER]:
            raise NotFound("No User matches the given query.")
        return Response(self.get_serializer(user).data)
