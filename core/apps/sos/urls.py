from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PositionView

router = DefaultRouter()
router.register('positon', PositionView, basename="position")

urlpatterns = [
    path("", include(router.urls)),
]
