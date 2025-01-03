from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PositionView, UserRequestView

router = DefaultRouter()
router.register("positon", PositionView, basename="position")
router.register("request", UserRequestView, basename="request")

urlpatterns = [
    path("", include(router.urls)),
]
