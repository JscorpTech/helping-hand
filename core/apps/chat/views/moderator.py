from typing import Any

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from core.apps.accounts.serializers import UserSerializer

from core.apps.accounts.choices import RoleChoice

from ..filters import ModeratorFilter
from django_core.paginations import CustomPagination
from ..serializers.chat import ListUserSerializer


@extend_schema(tags=["moderator"])
class ModeratorView(BaseViewSetMixin, GenericViewSet):
    pagination_class = None

    def get_serializer_context(self):
        data = super().get_serializer_context()
        match self.action:
            case "retrieve" | "list":
                data["type"] = "moderator"
        return data

    def get_serializer_class(self) -> Any:
        match self.action:
            case "retrieve" | "list":
                return UserSerializer
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
                enum=RoleChoice.moderator_roles(),
            ),
            OpenApiParameter(
                name="search",
                type=str,
                description="Search by first or last name",
                required=False,
            ),
        ],
        responses={200: UserSerializer(many=True)},
    )
    @method_decorator(cache_page(60))
    def list(self, request):
        users = get_user_model().objects.filter(role__in=RoleChoice.moderator_roles())
        paginator = CustomPagination()
        django_filter = ModeratorFilter(request.GET, queryset=users)
        if not django_filter.is_valid():
            raise ValidationError({"detail": django_filter.errors})
        queryset = paginator.paginate_queryset(django_filter.qs, request)
        return paginator.get_paginated_response(self.get_serializer(queryset, many=True).data)

    @extend_schema(responses={200: UserSerializer()})
    @method_decorator(cache_page(60))
    def retrieve(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        return Response(self.get_serializer(user).data)
