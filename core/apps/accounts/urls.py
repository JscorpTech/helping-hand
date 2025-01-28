"""
Accounts app urls
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from rest_framework_simplejwt import views as jwt_views

from .views import (
    ChangePasswordView,
    MeView,
    RegisterView,
    ResetPasswordView,
    UserView,
    CsTokenObtainPairView,
    CsTokenRefreshView,
    CsTokenVerifyView,
)

router = DefaultRouter()
router.register("auth", RegisterView, basename="auth")
router.register("auth", ResetPasswordView, basename="reset-password")
router.register("auth", MeView, basename="me")
router.register("auth", ChangePasswordView, basename="change-password")
router.register("users", UserView, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", CsTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/verify/", CsTokenVerifyView.as_view(), name="token_verify"),
    path(
        "auth/token/refresh/",
        CsTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
