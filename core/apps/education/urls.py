from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TutorialView

router = DefaultRouter()
router.register(r"tutorial", TutorialView, basename="tutorial")


urlpatterns = [
    path("", include(router.urls)),
]
