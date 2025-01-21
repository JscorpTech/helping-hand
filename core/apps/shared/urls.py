from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerView,FaqView

router = DefaultRouter()
router.register("banner", BannerView, "banner")
router.register("faq", FaqView,"faq")

urlpatterns = [
    path("", include(router.urls)),
]
