from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BannerView, DashboardView, FaqCategoryView, FaqView, NotificationView

router = DefaultRouter()
router.register("banner", BannerView, "banner")
router.register("faq-category", FaqCategoryView, "faq-category")
router.register("faq", FaqView, "faq")
router.register("dashboard", DashboardView, "dashboard")
router.register("notification", NotificationView, "notification")
# router.register("user-notification", UserNotificationView, "user-notification")

urlpatterns = [
    path("", include(router.urls)),
]
