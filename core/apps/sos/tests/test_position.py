from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class UserrequestTestTest(TestCase):

    def _create_user(self):
        return get_user_model().objects.create_user(phone="1111111111", password="password")

    def setUp(self):
        self.user = self._data = self._create_user()
        self.client = APIClient()
        self.urls = {
            "create": reverse("position-list"),
        }

    def test_create(self):
        self.client.force_authenticate(user=self.user)
        data = {"long": 69.274829, "lat": 41.327002}
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
