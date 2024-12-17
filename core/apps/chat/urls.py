from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupView, ModeratorView

router = DefaultRouter()
router.register("group", GroupView, basename="group")
router.register("moderator", ModeratorView, basename="moderator")

urlpatterns = [
    path("", include(router.urls)),
]
