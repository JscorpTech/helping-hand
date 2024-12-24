from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TutorialView, GuideView

router = DefaultRouter()
router.register(r"tutorial", TutorialView, basename="tutorial")
router.register(r"guide", GuideView, basename="guide")


urlpatterns = [
    path("", include(router.urls)),
]
