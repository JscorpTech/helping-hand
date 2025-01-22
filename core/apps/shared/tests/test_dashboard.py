from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

import logging


class DashboardTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(get_user_model()._create_fake_admin())
        self.urls = {
            "list": reverse("dashboard-list"),
        }

    def test_list(self):
        response = self.client.get(self.urls["list"])
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.status_code, 200)
