# from django.utils.translation import gettext_lazy as _  # noqa
# from django_core.mixins import BaseViewSetMixin
# from drf_spectacular.utils import extend_schema
# from rest_framework.permissions import AllowAny, IsAuthenticated  # noqa

# from ..serializers import (
#     UserCreateSerializer,
#     UserListSerializer,
#     UserRetrieveSerializer,
#     UserUpdateSerializer,
# )

# from drf_spectacular.utils import extend_schema  # noqa
# from django.contrib.auth import get_user_model
# from django_core.mixins import BaseViewSetMixin  # noqa

# from rest_framework.viewsets import ModelViewSet
# from ..permissions import AdminPermission

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from ..serializers import (
    CsTokenObtainPairSerializer,
    CsTokenRefreshSerializer,
    CsTokenVerifySerializer,
)


class CsTokenObtainPairView(TokenObtainPairView):
    serializer_class = CsTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        print("Custom Token Obtain Pair View Called!")
        return super().post(request, *args, **kwargs)


class CsTokenRefreshView(TokenRefreshView):
    serializer_class = CsTokenRefreshSerializer


class CsTokenVerifyView(TokenVerifyView):
    serializer_class = CsTokenVerifySerializer
