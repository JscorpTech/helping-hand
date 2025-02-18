from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class UserrequestTestTest(TestCase):

    def setUp(self):
        self.user = self._data = get_user_model()._create_fake_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.urls = {
            "list": reverse("position-list"),
            "retrieve": reverse("position-detail", kwargs={"pk": self.user.id}),
            "latest": reverse("position-latest", kwargs={"pk": self.user.id}),
        }

    def test_create(self):
        data = {"long": 69.274829, "lat": 41.327002}
        response = self.client.post(self.urls["list"], data)
        self.assertTrue(response.json()["status"])
        self.assertTrue(True)

    def test_update(self):
        self.assertTrue(True)

    def test_partial_update(self):
        self.assertTrue(True)

    def test_destroy(self):
        self.assertTrue(True)

    def test_latest(self):
        response = self.client.get(self.urls["latest"])
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        response = self.client.get(self.urls["retrieve"])
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)
