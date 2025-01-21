from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from ..models import FaqModel
import logging  # noqa


class FaqTest(TestCase):

    def _create_data(self):
        return FaqModel._create_fake()

    def setUp(self):
        self.client = APIClient()
        self.instance = self._create_data()
        self.client.force_authenticate(get_user_model()._create_fake_admin())
        self.urls = {
            "list": reverse("faq-list"),
            "retrieve": reverse("faq-detail", kwargs={"pk": self.instance.pk}),
            "retrieve-not-found": reverse("faq-detail", kwargs={"pk": 1000}),
        }


    def test_create(self):
        response = self.client.post(
            self.urls["list"],
            {
                "question": "question?",
                "answer": "answer!!",
            },
        )
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 201)


    def test_update(self):
        response = self.client.put(
            self.urls["retrieve"],
            {
                "question": "new question",
                "answer": "old answer",
            },
        )
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)


    def test_partial_update(self):
        response = self.client.patch(self.urls["retrieve"], {"question": "old question again"})
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
