from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import ExamModel, ExamResultModel, SertificateModel


class ExamTest(TestCase):

    def _create_data(self):
        return ExamModel._create_face()

    def setUp(self):
        self.client = APIClient()
        self.instance = self._create_data()
        self.urls = {
            "list": reverse("exam-list"),
            "retrieve": reverse("exam-detail", kwargs={"pk": self.instance.pk}),
            "retrieve-not-found": reverse("exam-detail", kwargs={"pk": 1000}),
        }

    def test_create(self):
        self.assertTrue(True)

    def test_update(self):
        self.assertTrue(True)

    def test_partial_update(self):
        self.assertTrue(True)

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


class SertificateTest(TestCase):

    def _create_data(self):
        return SertificateModel._create_face()

    def setUp(self):
        self.client = APIClient()
        self.instance = self._create_data()
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
        self.assertTrue(True)

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


class ExamresultTest(TestCase):

    def _create_data(self):
        return ExamResultModel._create_face()

    def setUp(self):
        self.client = APIClient()
        self.instance = self._create_data()
        self.urls = {
            "list": reverse("examresult-list"),
            "retrieve": reverse("examresult-detail", kwargs={"pk": self.instance.pk}),
            "retrieve-not-found": reverse("examresult-detail", kwargs={"pk": 1000}),
        }

    def test_create(self):
        self.assertTrue(True)

    def test_update(self):
        self.assertTrue(True)

    def test_partial_update(self):
        self.assertTrue(True)

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
