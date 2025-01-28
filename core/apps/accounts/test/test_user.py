from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.apps.accounts.models import AuthProviderChoice, User
from core.apps.accounts.serializers import UserSerializer


class UserViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(get_user_model()._create_fake_admin())
        self.phone = "998999999999"
        self.password = "password"
        self.instance = get_user_model().objects.create_user(
            phone=self.phone, first_name="John", last_name="Doe", password=self.password
        )
        self.urls = {
            "list": reverse("users-list"),
            "retrieve": reverse("users-detail", kwargs={"pk": self.instance.pk}),
            "retrieve-not-found": reverse("users-detail", kwargs={"pk": 1000}),
        }

    def test_create(self):
        response = self.client.post(
            self.urls["list"],
            {
                "phone": "998335190626",
                "username": "user9090",
                "bio": "biooooo",
                "password":"password",
                },
        )
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        response = self.client.put(
            self.urls["retrieve"],
            {
                "phone": "998335193726",
                "username": "user99999",
                "bio": "boiiiii",
                "password":"qwerty",
                },
        )
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)

    def test_partial_update(self):
        response = self.client.patch(self.urls["retrieve"], {"phone": "999999999999"})
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)

    def test_destroy(self):
        response = self.client.delete(self.urls["retrieve"])
        self.assertEqual(response.status_code, 204)

    def test_list(self):
        response = self.client.get(self.urls["list"])
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        response = self.client.get(self.urls["retrieve"])
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)

    def test_retrieve_not_found(self):
        response = self.client.get(self.urls["retrieve-not-found"])
        self.assertFalse(response.json()["status"])
        self.assertEqual(response.status_code, 404)
