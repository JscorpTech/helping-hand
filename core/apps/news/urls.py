from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostView

router = DefaultRouter()
router.register("post", PostView, basename="post")


urlpatterns = [
    path("", include(router.urls)),
]
