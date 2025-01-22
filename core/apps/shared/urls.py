from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerView, FaqView, DashboardView

router = DefaultRouter()
router.register("banner", BannerView, "banner")
router.register("faq", FaqView, "faq")
router.register("dashboard", DashboardView, "dashboard")

urlpatterns = [
    path("", include(router.urls)),
    # path("dashboard/", DashboardView.as_view(), name="dashboard")
]
