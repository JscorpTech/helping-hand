from typing import Any

from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_core.mixins import BaseViewSetMixin

from core.apps.news.models import PostModel
from core.apps.accounts.models import ModeratorModel
from core.apps.education.models import TutorialModel
from core.apps.education.models import SertificateModel, SertificateChoices

from ..serializers.dashboard import DashboardSerializer


extend_schema(tags=["dashboard"])


class DashboardView(BaseViewSetMixin, GenericViewSet):

    def list(self, request) -> Any:

        UserModel = get_user_model()
        users_count = UserModel.objects.count()

        news_count = PostModel.objects.count()

        moderators_count = ModeratorModel.objects.count()

        videos_count = TutorialModel.objects.filter(video__isnull=False).exclude(video__exact="").count()

        sertificated_users_count = SertificateModel.objects.filter(status__exact=SertificateChoices.ACTIVE).count()
        i_sertificated_users_count = SertificateModel.objects.filter(status__exact=SertificateChoices.INACTIVE).count()

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
