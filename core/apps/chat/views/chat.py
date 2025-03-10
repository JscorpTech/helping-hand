from typing import Any

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext as _
from django_core.mixins import BaseViewSetMixin
from django_core.paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.apps.accounts.permissions import AdminPermission

from ..models import GroupModel, MessageModel
from ..serializers.chat import (
    CreateGroupSerializer,
    CreateMessageSerializer,
    CreatePublicGroupSerializer,
    ListGroupSerializer,
    ListMessageSerializer,
    RetrieveGroupSerializer,
    WsGroupSerializer,
    WsMessageSerializer,
)


@extend_schema(tags=["group"])
class GroupView(BaseViewSetMixin, ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["chat_type", "is_public"]
    search_fields = ["name"]

    def _send_ws_message(self, group, data):
        # Send message to group
        async_to_sync(get_channel_layer().group_send)(
            group,
            {
                "type": "chat_message",
                **data,
            },
        )

    def get_queryset(self):
        queryset = GroupModel.objects.order_by("-created_at")
        if self.request.user.is_authenticated:
            queryset = queryset.filter(models.Q(users__in=[self.request.user]) | models.Q(is_public=True))
        else:
            queryset = queryset.filter(is_public=True)
        return queryset.all()

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list":
                return ListGroupSerializer
            case "create" | "update" | "partial_update":
                return CreatePublicGroupSerializer
            case "retrieve":
                return RetrieveGroupSerializer
            case "create_group":
                return CreateGroupSerializer
            case "get_messages":
                return ListMessageSerializer
            case "send_message" | "update_message":
                return CreateMessageSerializer
            case _:
                return ListGroupSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case (
                "send_message"
                | "update_message"
                | "delete_message"
                | "create_group"
                | "read_all_messages"
                | "read_message"
            ):
                perms.extend([IsAuthenticated])
            case "create" | "delete" | "delete_destroy":
                perms.extend([IsAuthenticated, AdminPermission])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()

    @extend_schema(summary="Yangi guruh yaratish Admin")
    def create(self, request, *args, **kwargs):
        """Yangi guruh yaratish"""
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="Guruhni o'chirish admin")
    def destroy(self, request, *args, **kwargs):
        """Guruhni o'chirish"""
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(is_public=True)

    @action(methods=["POST"], detail=False, url_name="create-group", url_path="create-group")
    def create_group(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.validated_data.get("user")
        group = GroupModel.objects.filter(
            users__in=[request.user, user],
            is_public=False,
            chat_type=user.role,
        )
        if group.exists():
            return Response(
                {
                    "detail": _("You already have a group with this user"),
                    "group_id": group.first().id,
                    "is_new": False,
                },
                status=status.HTTP_200_OK,
            )
        group = GroupModel.objects.create(
            name="%s-%s" % (request.user.full_name, user.full_name),
            chat_type=user.role,
            image=ser.validated_data.get("image", None),
        )
        group.users.add(request.user, user)
        self._send_ws_message(
            user.username,
            {"action": "create_group", "data": WsGroupSerializer(group, context={"request": request}).data},
        )
        try:
            async_to_sync(get_channel_layer().group_add)(
                f"group_{group.id}",
                cache.get("channel_%s" % user.username),
            )
        except Exception as e:
            print(e)
        return Response(
            {
                "detail": _("Group created successfully"),
                "group_id": group.id,
                "is_new": True,
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string", "example": "Message updated successfully"},
                        "message_id": {"type": "integer", "example": 1},
                    },
                },
                description="Successful response with additional metadata",
            )
        }
    )
    @action(methods=["POST"], detail=True, url_path="update-message/(?P<message_id>[0-9]+)")
    def update_message(self, request, pk, message_id):
        message = MessageModel.objects.filter(id=message_id, group_id=pk, user_id=request.user.id)
        if not message.exists():
            raise NotFound(_("Message not found"))
        ser = self.get_serializer(
            message.first(),
            data=request.data,
            partial=True,
        )
        ser.is_valid(raise_exception=True)
        ser.save()
        self._send_ws_message(
            f"group_{pk}",
            {
                "action": "update_message",
                "data": WsMessageSerializer(ser.instance).data,
            },
        )
        return Response({"detail": _("Message updated successfully"), "message_id": int(message_id)})

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string", "example": "Message deleted successfully"},
                        "message_id": {"type": "integer", "example": 1},
                    },
                },
                description="Successful response with additional metadata",
            )
        }
    )
    @action(methods=["POST"], detail=True, url_path="delete-message/(?P<message_id>[0-9]+)")
    def delete_message(self, request, pk, message_id):
        message = MessageModel.objects.filter(id=message_id, group_id=pk, user_id=request.user.id)
        if not message.exists():
            raise NotFound(_("Message not found"))
        message.delete()
        self._send_ws_message(
            f"group_{pk}",
            {
                "action": "delete_message",
                "data": {"id": pk},
            },
        )
        return Response({"detail": _("Message deleted successfully"), "message_id": int(message_id)})

    @extend_schema(
        responses={
            200: OpenApiResponse(
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
        if not GroupModel.objects.filter(id=pk).exists():
            raise NotFound(_("Group not found"))
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(group_id=pk, user_id=request.user.id)
        self._send_ws_message(
            f"group_{pk}",
            {
                "action": "send_message",
                "data": WsMessageSerializer(ser.instance, context={"request": request}).data,
            },
        )
        return Response(
            {"detail": _("Message sent successfully"), "message_id": ser.instance.id}, status=status.HTTP_201_CREATED
        )

    @action(methods=["GET"], detail=True, url_path="get-messages")
    def get_messages(self, request, pk):
        paginator = CustomPagination()
        paginator.page_size = 50
        queryset = paginator.paginate_queryset(
            MessageModel.objects.order_by("-created_at").filter(group_id=pk), request
        )
        return paginator.get_paginated_response(self.get_serializer(reversed(queryset), many=True).data)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string", "example": "Message marked as read successfully"},
                    },
                },
                description="Successful response with additional metadata",
            )
        }
    )
    @action(methods=["POST"], detail=True, url_path="read-message/(?P<message_id>[0-9]+)")
    def read_message(self, request, pk, message_id):
        message = MessageModel.objects.filter(id=message_id, group_id=pk)
        if not message.exists():
            raise NotFound(_("Message not found"))
        message.update(is_read=True)
        return Response({"detail": _("Message marked as read successfully"), "message_id": int(message_id)})

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string", "example": "All messages marked as read successfully"},
                    },
                },
                description="Successful response with additional metadata",
            )
        }
    )
    @action(methods=["POST"], detail=True, url_path="read-all-messages")
    def read_all_messages(self, request, pk):
        messages = MessageModel.objects.filter(group_id=pk, is_read=False).exclude(user__in=[request.user])
        messages.update(is_read=True)
        return Response(
            {"detail": _("All messages marked as read successfully"), "messages": messages.values_list("id", flat=True)}
        )
