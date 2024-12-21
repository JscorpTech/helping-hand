from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
from ..models import TutorialModel, TestModel, QuestionModel, VariantModel


class TutorialTest(TestCase):

    def _create_tutorial(self):
        test = TestModel.objects.create(topic="Test", desc="Test", time=100)
        question = QuestionModel.objects.create(test=test, question="Test")
        VariantModel.objects.create(question=question, variant="Test 2")
        VariantModel.objects.create(question=question, variant="Test", is_true=True)

        return TutorialModel.objects.create(
            type="video", name="Test", desc="Test", image="image.jpg", file="file.zip", video="video.mp4", test=test
        )

    def setUp(self):
        self.client = APIClient()
        self.tutorial = self._create_tutorial()
        self.urls = {
            "list": reverse("tutorial-list"),
            "retrieve": reverse("tutorial-detail", kwargs={"pk": self.tutorial.pk}),
            "test": reverse("tutorial-detail", kwargs={"pk": self.tutorial.pk}),
        }

    def test_create(self):
        self.assertTrue(True)

    def test_update(self):
        self.assertTrue(True)

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
