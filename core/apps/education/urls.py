from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExamView, GuideView, QuestionView, SertificateView, TutorialView

router = DefaultRouter()
router.register(r"tutorial", TutorialView, basename="tutorial")
router.register(r"guide", GuideView, basename="guide")
router.register(r"question", QuestionView, basename="question")
router.register(r"sertificate", SertificateView, basename="sertificate")
router.register(r"", ExamView, basename="exam")


urlpatterns = [
    path("", include(router.urls)),
]
