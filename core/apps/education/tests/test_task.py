from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import TaskModel, TutorialModel


class TaskTest(TestCase):

    def _create_tutorial(self):
        return TutorialModel.objects.create(
            name="Test", desc="Test", image="image.jpg", file="file.zip", video="video.mp4", task=self._create_data()
        )

    def _create_data(self):
        return TaskModel._create_fake()

    def setUp(self):
        self.client = APIClient()
        self.instance = self._create_tutorial()
        self.urls = {
            "get": reverse("tutorial-task", kwargs={"pk": self.instance.pk}),
            "answer": reverse("tutorial-task-answer", kwargs={"pk": self.instance.pk}),
        }

    def test_get(self):
        response = self.client.get(self.urls["get"])
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)

    def test_answer(self):
        self.client.force_authenticate(get_user_model()._create_fake())
        response = self.client.post(self.urls["answer"], {"answer": "Salom bratishka"})
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)

    def test_not_auth_answer(self):
        response = self.client.post(self.urls["answer"], {"answer": "Salom bratishka"})
        self.assertFalse(response.json()["status"])
        self.assertEqual(response.status_code, 401)
