from typing import Any

from asgiref.sync import async_to_sync
from channels.consumer import get_channel_layer
from django.contrib.gis.geos import Point
from django.utils.translation import gettext as _
from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import GenericViewSet

from ..models import PositionModel
from ..permissions import PositionPermission
from ..serializers.position import CreatePositionSerializer, ListPositionSerializer, RetrievePositionSerializer


@extend_schema(tags=["sos"])
class PositionView(
    BaseViewSetMixin,
    GenericViewSet,
):
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return PositionModel.objects.all()

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list":
                return ListPositionSerializer
            case "retrieve":
                return RetrievePositionSerializer
            case "create":
                return CreatePositionSerializer
            case _:
                return ListPositionSerializer

    def get_permissions(self) -> Any:
        perms = [IsAuthenticated]
        match self.action:
            case "retrieve" | "latest":
                perms.extend([PositionPermission])
        self.permission_classes = perms
        return super().get_permissions()

    @extend_schema(responses={200: ListPositionSerializer(many=True)})
    def retrieve(self, reuqest, pk):
        positions = PositionModel.objects.filter(user_id=pk).order_by("-created_at")
        return Response(self.get_serializer(positions, many=True).data)

    @extend_schema(responses={200: ListPositionSerializer})
    @action(methods=["GET"], detail=True, url_path="latest", url_name="latest")
    def latest(self, reuqest, pk):
        positions = PositionModel.objects.filter(user_id=pk).order_by("-created_at").first()
        return Response(self.get_serializer(positions).data)

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response={"type": "object"},
                examples=[
                    OpenApiExample("Example", value={"status": True, "data": {"detail": "Joylashuv saqlandi"}}),
                ],
            )
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        location = Point(data.get("lat"), data.get("long"))
        position = PositionModel.objects.create(location=location, user=request.user)
        async_to_sync(get_channel_layer().group_send)(
            f"user_{request.user.id}",
            {
                "type": "position",
                "status": True,
                "data": {
                    "id": position.id,
                    "long": data["long"],
                    "lat": data["lat"],
                    "created_at": position.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                    "updated_at": position.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                },
            },
        )
        return Response({"detail": _("Joylashuv saqlandi")}, status=status.HTTP_201_CREATED)
