from typing import Any

from django.db import models
from django.utils.translation import gettext as _
from django_core.mixins import BaseViewSetMixin
from django_core.paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ..models import GroupModel, MessageModel
from ..serializers.chat import (
    CreateGroupSerializer,
    CreateMessageSerializer,
    ListGroupSerializer,
    ListMessageSerializer,
    RetrieveGroupSerializer,
    WsMessageSerializer,
)


@extend_schema(tags=["group"])
class GroupView(BaseViewSetMixin, ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["chat_type", "is_public"]

    def get_queryset(self):
        queryset = GroupModel.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(models.Q(users__in=[self.request.user]) | models.Q(is_public=True))
        else:
            queryset = queryset.filter(is_public=True)
        return queryset

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list":
                return ListGroupSerializer
            case "retrieve":
                return RetrieveGroupSerializer
            case "create":
                return CreateGroupSerializer
            case "get_messages":
                return ListMessageSerializer
            case "send_message":
                return CreateMessageSerializer
            case _:
                return ListGroupSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "send_message":
                perms.extend([IsAuthenticated])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string", "example": "Message sent successfully"},
                    },
                },
                description="Successful response with additional metadata",
            )
        }
    )
    @action(methods=["POST"], detail=True, url_path="send-message")
    def send_message(self, request, pk):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(group_id=pk, user_id=request.user.id)
        async_to_sync(get_channel_layer().group_send)(
            f"group_{pk}",
            {
                "type": "chat_message",
                "data": WsMessageSerializer(ser.instance).data,
            },
        )
        return Response({"detail": _("Message sent successfully")}, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=True, url_path="get-messages")
    def get_messages(self, request, pk):
        paginator = CustomPagination()
        paginator.page_size = 50
        queryset = paginator.paginate_queryset(
            MessageModel.objects.order_by("-created_at").filter(group_id=pk), request
        )
        return paginator.get_paginated_response(self.get_serializer(reversed(queryset), many=True).data)
