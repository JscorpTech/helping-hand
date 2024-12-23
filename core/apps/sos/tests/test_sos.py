from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model


class UserrequestTestTest(TestCase):

    def _create_user(self):
        return get_user_model().objects.create_user(phone="1111111111", password="password")

    def setUp(self):
        self.user = self._data = self._create_user()
        self.client = APIClient()
        self.urls = {
            "create": reverse("request-list"),
        }

    def test_create(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "area": "unsafe",
        }
        response = self.client.post(self.urls["create"], data)
        self.assertTrue(response.json()["status"])
        self.assertTrue(True)

    def test_update(self):
        self.assertTrue(True)

    def test_partial_update(self):
        self.assertTrue(True)

    def test_destroy(self):
        self.assertTrue(True)

    # def test_list(self):
    #     response = self.client.get(self.urls["list"])
    #     self.assertTrue(response.json()["status"])
    #     self.assertEqual(response.status_code, 200)

    # def test_retrieve(self):
    #     response = self.client.get(self.urls["retrieve"])
    #     self.assertTrue(response.json()["status"])
    #     self.assertEqual(response.status_code, 200)
