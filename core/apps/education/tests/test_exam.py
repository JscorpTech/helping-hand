from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import ExamModel


class ExamTest(TestCase):

    def _create_data(self):
        return ExamModel._create_fake()

    def setUp(self):
        self.client = APIClient()
        self.instance = self._create_data()
        self.urls = {
            "detail": reverse("exam-exam"),
        }

    def test_create(self):
        self.assertTrue(True)

    def test_update(self):
        self.assertTrue(True)

    def test_partial_update(self):
        self.assertTrue(True)

    def test_destroy(self):
        self.assertTrue(True)

    def test_detail(self):
        response = self.client.get(self.urls["detail"])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.json()["data"]["id"], self.instance.id)
