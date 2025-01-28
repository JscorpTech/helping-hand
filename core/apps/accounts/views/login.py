from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from ..serializers import CsTokenObtainPairSerializer, CsTokenRefreshSerializer, CsTokenVerifySerializer


class CsTokenObtainPairView(TokenObtainPairView):
    serializer_class = CsTokenObtainPairSerializer


class CsTokenRefreshView(TokenRefreshView):
    serializer_class = CsTokenRefreshSerializer


class CsTokenVerifyView(TokenVerifyView):
    serializer_class = CsTokenVerifySerializer
