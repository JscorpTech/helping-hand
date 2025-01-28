from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated  # noqa
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import NotificationModel, UserNotificationModel
from ..serializers import CreateNotificationSerializer, RetrieveNotificationSerializer, UserNotificationSerializer


@extend_schema(tags=["notification"])
class NotificationView(BaseViewSetMixin, ModelViewSet):
    queryset = NotificationModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CreateNotificationSerializer
    action_serializer_class = {
        "create": CreateNotificationSerializer,
        "list": UserNotificationSerializer,
        "retrieve": RetrieveNotificationSerializer,
    }
    action_permission_classes = {
        "list": [IsAuthenticated],
    }

    def list(self, request, *args, **kwargs):
        user_notifications = UserNotificationModel.objects.filter(user=self.request.user)
        print(user_notifications)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(user_notifications, many=True)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
