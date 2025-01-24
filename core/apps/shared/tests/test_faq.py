from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from ..models import FaqModel, FaqCategoryModel
import logging  # noqa


class FaqCategoryTest(TestCase):

    def _create_data(self):
        return FaqCategoryModel._create_fake()

    def setUp(self):
        self.client = APIClient()
        self.instance = self._create_data()
        self.client.force_authenticate(get_user_model()._create_fake_admin())
        self.urls = {
            "list": reverse("faq-category-list"),
            "retrieve": reverse("faq-category-detail", kwargs={"pk": self.instance.pk}),
            "retrieve-not-found": reverse("faq-category-detail", kwargs={"pk": 1000}),
        }

    def test_create(self):
        response = self.client.post(
            self.urls["list"],
            {
                "name": "teessstttt",
            },
        )
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        response = self.client.put(
            self.urls["retrieve"],
            {
                "name": "updated_test",
            },
        )
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


class FaqTest(TestCase):

    def _create_data(self):
        self.faq_category = FaqCategoryModel.objects.create(name="TEST")
        print(self.faq_category.id, self.faq_category, "\n\n\n\n")
        return FaqModel.objects.create(category=self.faq_category, question="test_q", answer="test_a")

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
                "category": self.faq_category.pk,
                "question": "question?",
                "answer": "answer!!",
            },
        )
        logging.error(response.json())
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        response = self.client.put(
            self.urls["retrieve"],
            {
                "category": self.faq_category.pk,
                "question": "new question",
                "answer": "old answer",
            },
        )
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)

    def test_partial_update(self):
        response = self.client.patch(self.urls["retrieve"], {"question": "old question again@@@"})
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
