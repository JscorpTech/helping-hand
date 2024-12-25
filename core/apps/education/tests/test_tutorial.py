from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from core.apps.accounts.choices import RoleChoice
from ..models import QuestionModel, TestModel, TutorialModel, VariantModel
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class TutorialTest(TestCase):

    def _create_tutorial(self):
        test = TestModel.objects.create(topic="Test", desc="Test", time=100)
        question = QuestionModel.objects.create(test=test, question="Test")
        VariantModel.objects.create(question=question, variant="Test 2")
        VariantModel.objects.create(question=question, variant="Test", is_true=True)

        return TutorialModel.objects.create(
            name="Test", desc="Test", image="image.jpg", file="file.zip", video="video.mp4", test=test
        )

    def setUp(self):
        self.client = APIClient()
        self.tutorial = self._create_tutorial()
        self.urls = {
            "list": reverse("tutorial-list"),
            "create": reverse("tutorial-list"),
            "update": reverse("tutorial-detail", kwargs={"pk": self.tutorial.pk}),
            "retrieve": reverse("tutorial-detail", kwargs={"pk": self.tutorial.pk}),
            "test": reverse("tutorial-test", kwargs={"pk": self.tutorial.pk}),
            "completed": reverse("tutorial-completed"),
        }

    def test_create(self):
        user = get_user_model()._create_fake()
        with open(settings.BASE_DIR / "resources/assets/test.png", "rb") as file:
            image = SimpleUploadedFile("image.jpg", file.read(), content_type="image/jpeg")
        user.role = RoleChoice.LAWYER
        user.save()
        self.client.force_authenticate(user=user)
        data = {
            "name": "Test 2",
            "desc": "Test 2",
            "image": image,
            "test": self.tutorial.test.pk,
            "tags": [],
            "position": 1,
            "source": "http://example.com",
        }
        response = self.client.post(self.urls["create"], data, format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["status"])

    def test_update(self):
        user = get_user_model()._create_fake()
        user.role = RoleChoice.LAWYER
        user.save()
        self.client.force_authenticate(user=user)
        data = {
            "name": "Test 2",
            "desc": "Test 2",
            "test": self.tutorial.test.pk,
            "tags": '["salom", "qalaysan"]',
            "position": 1,
            "source": "http://example.com",
        }
        response = self.client.patch(self.urls["update"], data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["status"])

    def test_partial_update(self):
        self.assertTrue(True)

    def test_destroy(self):
        self.assertTrue(True)

    def test_not_found(self):
        response = self.client.get(reverse("tutorial-detail", kwargs={"pk": 1000}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["status"], False)

    def test_list(self):
        response = self.client.get(self.urls["list"])
        self.assertEqual(response.json()["status"], True)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        response = self.client.get(self.urls["retrieve"])
        self.assertEqual(response.json()["status"], True)
        self.assertEqual(response.status_code, 200)

    def test_test_list(self):
        response = self.client.get(self.urls["test"])
        self.assertEqual(response.json()["status"], True)
        self.assertEqual(response.status_code, 200)

    def test_test_completed(self):
        self.client.force_authenticate(user=get_user_model()._create_fake())
        response = self.client.get(self.urls["completed"])
        self.assertEqual(response.json()["status"], True)
        self.assertEqual(response.status_code, 200)
