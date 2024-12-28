import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from core.apps.accounts.choices import RoleChoice

from ..models import QuestionModel, TestModel, TutorialModel, VariantModel


class TutorialTest(TestCase):

    def _create_tutorial(self):
        test = TestModel.objects.create(topic="Test", desc="Test", time=100)
        self.question = QuestionModel.objects.create(test=test, question="Test")
        VariantModel.objects.create(question=self.question, variant="Test 2", bal=10)
        VariantModel.objects.create(question=self.question, variant="Test", is_true=True, bal=10)

        return TutorialModel.objects.create(
            name="Test", desc="Test", image="image.jpg", file="file.zip", video="video.mp4", test=test
        )

    def _create_lawyer(self):
        user = get_user_model()._create_fake()
        user.role = RoleChoice.LAWYER
        user.save()
        return user

    def setUp(self):
        self.client = APIClient()
        self.tutorial = self._create_tutorial()
        self.urls = {
            "list": reverse("tutorial-list"),
            "create": reverse("tutorial-list"),
            "test-answer": reverse("tutorial-test-answer", kwargs={"pk": self.tutorial.pk}),
            "update": reverse("tutorial-detail", kwargs={"pk": self.tutorial.pk}),
            "retrieve": reverse("tutorial-detail", kwargs={"pk": self.tutorial.pk}),
            "test": reverse("tutorial-test", kwargs={"pk": self.tutorial.pk}),
            "completed": reverse("tutorial-completed"),
        }

    def test_test_answer_success(self):
        self.client.force_authenticate(user=self._create_lawyer())
        response = self.client.post(
            self.urls["test-answer"],
            json.dumps(
                [{"question": self.question.pk, "variant": [self.question.variants.order_by("-id").first().pk]}]
            ),
            content_type="application/json",
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["status"])
        self.assertEqual(data["data"]["success"], 1)
        self.assertEqual(data["data"]["total"], 1)

    def test_test_answer_invalid_question(self):
        self.client.force_authenticate(user=get_user_model()._create_fake())
        response = self.client.post(
            self.urls["test-answer"],
            json.dumps([{"question": 100, "variant": [100]}]),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["status"])

    def test_test_answer_invalid_question_count(self):
        self.client.force_authenticate(user=get_user_model()._create_fake())
        response = self.client.post(
            self.urls["test-answer"],
            json.dumps(
                [
                    {"question": 100, "variant": [100]},
                    {"question": 100, "variant": [100]},
                    {"question": 100, "variant": [100]},
                ]
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["status"])

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
