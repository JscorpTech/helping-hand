import logging  # noqa

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import BannerModel


class BannerTest(TestCase):

    def _create_data(self):
        return BannerModel._create_fake()

    def setUp(self):
        self.client = APIClient()
        self.instance = self._create_data()
        self.client.force_authenticate(get_user_model()._create_fake_admin())
        self.urls = {
            "list": reverse("banner-list"),
            "retrieve": reverse("banner-detail", kwargs={"pk": self.instance.pk}),
            "retrieve-not-found": reverse("banner-detail", kwargs={"pk": 1000}),
        }

    def test_create(self):
        response = self.client.post(
            self.urls["list"],
            {
                "image": open("resources/assets/test.png", "rb"),
                "title": "title",
                "subtitle": "subtitle",
            },
        )
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        response = self.client.put(
            self.urls["retrieve"],
            {
                "title": "new title",
                "subtitle": "new subtitle",
                "image": open("resources/assets/test.png", "rb"),
            },
        )
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)

    def test_partial_update(self):
        response = self.client.patch(self.urls["retrieve"], {"title": "new title"})
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
