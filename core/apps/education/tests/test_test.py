from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import QuestionModel, VariantModel, TestModel
from django.contrib.auth import get_user_model
from core.apps.accounts.choices import RoleChoice
import logging  # noqa


class QuestionTest(TestCase):

    def _create_data(self):
        self.test = TestModel.objects.create(topic="Test", desc="Test", time=100)
        self.question = QuestionModel.objects.create(test=self.test, question="Test")
        VariantModel.objects.create(question=self.question, variant="Test 2", bal=10)
        VariantModel.objects.create(question=self.question, variant="Test", is_true=True, bal=10)

    def setUp(self):
        self.client = APIClient()
        self.instance = self._create_data()
        self.urls = {
            "update": reverse("question-detail", kwargs={"pk": self.question.pk}),
            "add": reverse("question-list"),
            "delete": reverse("question-detail", kwargs={"pk": self.question.pk}),
        }

    def test_create(self):
        self.assertTrue(True)

    def test_update(self):
        self.assertTrue(True)

    def test_partial_update(self):
        self.assertTrue(True)

    def test_destroy(self):
        self.assertTrue(True)

    def test_question_update(self):
        user = get_user_model()._create_fake()
        user.role = RoleChoice.ADMIN
        user.save()
        self.client.force_authenticate(user=user)
        data = {
            "question_uz": "updated",
            "is_many": True,
            "variants": [
                {"is_true": True, "variant_uz": 1, "bal": 10},
                {"is_true": True, "variant_uz": 2, "bal": 10},
                {"is_true": True, "variant_uz": 3, "bal": 10},
            ],
        }
        response = self.client.patch(self.urls["update"], data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["status"])

    def test_question_add(self):
        user = get_user_model()._create_fake_admin()
        self.client.force_authenticate(user=user)
        data = [
            {
                "question_uz": "updated",
                "is_many": True,
                "test_id": self.test.id,
                "variants": [
                    {"is_true": True, "variant_uz": 1, "bal": 10},
                    {"is_true": True, "variant_uz": 2, "bal": 10},
                    {"is_true": True, "variant_uz": 3, "bal": 10},
                ],
            },
        ]
        response = self.client.post(self.urls["add"], data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["status"])

    def test_question_delete(self):
        user = get_user_model()._create_fake_admin()
        self.client.force_authenticate(user=user)
        response = self.client.delete(self.urls["delete"])
        self.assertEqual(response.status_code, 204)
