from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken


class CsTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active:
            raise AuthenticationFailed("Your account is disabled. Please contact support.")
        return data


class CsTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        try:
            refresh = RefreshToken(attrs["refresh"])
        except Exception:
            raise InvalidToken("Invalid refresh token provided.")

        user_id = refresh["user_id"]

        try:
            user = get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            raise AuthenticationFailed("User does not exist.")

        if not user.is_active:
            raise AuthenticationFailed("Your account is disabled. Please contact support.")

        return data


class CsTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        try:
            token = UntypedToken(attrs["token"])
        except Exception:
            raise AuthenticationFailed("Invalid token.")

        user_id = token.payload.get("user_id")

        try:
            user = get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            raise AuthenticationFailed("User does not exist.")

        if not user.is_active:
            raise AuthenticationFailed("Your account is disabled. Please contact support.")

        return data
