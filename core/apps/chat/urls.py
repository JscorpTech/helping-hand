from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupView

router = DefaultRouter()
router.register("group", GroupView, basename="group")

urlpatterns = [
    path("", include(router.urls)),
]
