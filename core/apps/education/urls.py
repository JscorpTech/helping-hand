from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TutorialView

router = DefaultRouter()
router.register(r"tutorial", TutorialView, basename="tutorial")


urlpatterns = [
    path("", include(router.urls)),
]
