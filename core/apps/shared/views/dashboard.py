from typing import Any

from django.contrib.auth import get_user_model
from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.apps.accounts.models import ModeratorModel
from core.apps.education.models import SertificateChoices, SertificateModel, TutorialModel
from core.apps.news.models import PostModel

from ..serializers.dashboard import DashboardSerializer
from ..services import get_userrequest_chart_data


@extend_schema(tags=["dashboard"])
class DashboardView(BaseViewSetMixin, GenericViewSet):
    serializer_class = DashboardSerializer
    periods = [
        "day",
        "week",
        "month",
        "year",
    ]

    @extend_schema(
        responses={
            200: {
                "type": "object",
                "properties": {
                    "labels": {"type": "array", "items": {"type": "string"}},
                    "data": {"type": "array", "items": {"type": "number"}},
                },
            }
        }
    )
    @action(methods=["GET"], detail=False, url_name="chart", url_path="chart/(?P<period>[a-zA-Z]+)")
    def chart(self, request, period):
        """
        period: day, week, month, year
        """
        if period not in self.periods:
            return Response({"detail": "period not found"})
        labels, chart_data = get_userrequest_chart_data(period)
        return Response({"labels": labels, "data": chart_data})

    def list(self, request) -> Any:

        UserModel = get_user_model()
        users_count = UserModel.objects.count()

        news_count = PostModel.objects.count()

        moderators_count = ModeratorModel.objects.count()

        videos_count = TutorialModel.objects.filter(video__isnull=False).exclude(video__exact="").count()

        sertificated_users_count = SertificateModel.objects.filter(status__exact=SertificateChoices.ACTIVE).count()

        endangered_users_count = "1"

        data = {
            "users_count": users_count,
            "news_count": news_count,
            "moderators_count": moderators_count,
            "videos_count": videos_count,
            "sertificated_users_count": sertificated_users_count,
            "endangered_users_count": endangered_users_count,
        }
        serializered_data = DashboardSerializer(data)
        return Response(data=serializered_data.data)

    def get_permissions(self) -> Any:
        perms = []
        match self.request.method:
            case "GET":
                perms.extend([AllowAny])

        self.permission_classes = perms
        return super().get_permissions()
