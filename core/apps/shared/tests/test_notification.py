from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from core.apps.accounts.choices import RoleChoice  # noqa
from ..models import NotificationModel, UserNotificationModel  # noqa
import logging  # noqa


class NotificationTest(TestCase):

    def _create_data(self):
        fake = NotificationModel.objects.create(
            title="test_title1",
            body="test_body1",
        )
        fake.users.add(self.test_user)
        return fake

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(get_user_model()._create_fake_admin())
        self.test_user = get_user_model()._create_fake()
        self.instance = self._create_data()
        self.urls = {
            "list": reverse("notification-list"),
            "retrieve": reverse("notification-detail", kwargs={"pk": self.instance.pk}),
            "retrieve-not-found": reverse("notification-detail", kwargs={"pk": 1000}),
        }

    def test_create(self):
        response = self.client.post(
            self.urls["list"],
            {
                "title": "create_title",
                "body": "create_body",
            },
        )
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        response = self.client.put(
            self.urls["retrieve"],
            {
                "title": "update_title",
                "body": "update_body",
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
