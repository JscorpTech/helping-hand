from typing import Any

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_core.mixins import BaseViewSetMixin
from django_core.paginations import CustomPagination
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


from core.apps.accounts.choices import RoleChoice
from core.apps.accounts.permissions import AdminPermission
from core.apps.accounts.serializers import CreateModeratorSerializer, UserSerializer

from ..filters import ModeratorFilter
from ..serializers.chat import ListUserSerializer


@extend_schema(tags=["moderator"])
class ModeratorView(BaseViewSetMixin, GenericViewSet):
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["role", "experience__lte", "level__lte"]
    search_fields = ["first_name", "last_name", "phone"]

    def get_serializer_context(self):
        data = super().get_serializer_context()
        match self.action:
            case "retrieve" | "list":
                data["type"] = "moderator"
        return data

    def get_serializer_class(self) -> Any:
        match self.action:
            case "create" | "update" | "partial_update":
                return CreateModeratorSerializer
            case "retrieve" | "list":
                return UserSerializer
            case _:
                return ListUserSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "create" | "update" | "partial_update" | "destroy":
                perms.extend([IsAuthenticated, AdminPermission])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()

    @extend_schema(summary="Moderator yaratish Admin")
    def create(self, request, *args, **kwargs):
        """Moderator yaratish"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            self.get_serializer({"id": serializer.instance.id, **serializer.validated_data}).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(summary="Moderator malumotlarini yangilash Admin")
    def update(self, request, pk, *args, **kwargs):
        """Moderator malumotlarini yangilash"""
        serializer = self.get_serializer(instance=get_object_or_404(get_user_model(), pk=pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "Moderator malumotlari yangilandi",
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(summary="Moderator malumotlarini yangilash Admin")
    def partial_update(self, request, pk, *args, **kwargs):
        """Moderator malumotlarini yangilash"""
        serializer = self.get_serializer(
            instance=get_object_or_404(get_user_model(), pk=pk), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "Moderator malumotlari yangilandi",
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(summary="Moderatorni o'chirish Admin")
    def destroy(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        user.delete()
        return Response({"detail": _("Moderator o'chirildi")})

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
    def list(self, request):
        users = get_user_model().objects.order_by("-created_at").filter(role__in=RoleChoice.moderator_roles())
        paginator = CustomPagination()
        django_filter = ModeratorFilter(request.GET, queryset=users)
        if not django_filter.is_valid():
            raise ValidationError({"detail": django_filter.errors})
        queryset = paginator.paginate_queryset(django_filter.qs, request)
        return paginator.get_paginated_response(self.get_serializer(queryset, many=True).data)

    @extend_schema(responses={200: UserSerializer()})
    def retrieve(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        return Response(self.get_serializer(user).data)
