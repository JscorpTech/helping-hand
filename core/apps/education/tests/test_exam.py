from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
import logging  # noqa

from ..models import ExamModel, SertificateModel

from django.contrib.auth import get_user_model


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


class SertificateTest(TestCase):

    def _create_data(self):
        return SertificateModel._create_fake()

    def setUp(self):
        self.client = APIClient()
        self.instance = self._create_data()
        self.client.force_authenticate(get_user_model()._create_fake_admin())
        self.urls = {
            "list": reverse("sertificate-list"),
            "retrieve": reverse("sertificate-detail", kwargs={"pk": self.instance.pk}),
            "retrieve-not-found": reverse("sertificate-detail", kwargs={"pk": 1000}),
        }

    def test_create(self):
        self.assertTrue(True)

    def test_update(self):
        self.assertTrue(True)

    def test_partial_update(self):
        response = self.client.patch(
            self.urls["retrieve"],
            {
                "status": "active"
            },
        )
        self.assertTrue(response.json()["status"])
        self.assertEqual(
            response.status_code, 200
        )

    def test_destroy(self):
        self.assertTrue(True)

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
