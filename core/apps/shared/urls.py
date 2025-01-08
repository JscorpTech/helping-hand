from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerView

router = DefaultRouter()
router.register("banner", BannerView, "banner")


urlpatterns = [
    path("", include(router.urls)),
]
