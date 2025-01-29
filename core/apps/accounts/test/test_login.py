from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status  # noqa
from rest_framework.test import APIClient

from core.apps.accounts.models import AuthProviderChoice, User  # noqa
from core.apps.accounts.serializers import UserSerializer  # noqa

# from logging import log


class LoginTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(get_user_model()._create_fake_admin())
        self.phone1 = "99899999999"
        self.phone2 = "99888888888"
        self.password = "password"
        self.instance1 = get_user_model().objects.create_user(
            phone=self.phone1, first_name="John", last_name="Doe", password=self.password
        )
        self.instance2 = get_user_model().objects.create_user(
            phone=self.phone2,
            first_name="John",
            last_name="Doe",
            password=self.password,
            is_active=True,
        )
        self.urls = {
            "auth-create": reverse("token_obtain_pair"),
            "auth-refresh": reverse("token_refresh"),
            "auth-verify": reverse("token_verify"),
        }

        response = self.client.post(self.urls["auth-create"], {"phone": self.phone1, "password": self.password})
        self.refresh1 = response.json().get("refresh")
        response = self.client.post(self.urls["auth-create"], {"phone": self.phone2, "password": self.password})
        self.refresh2 = response.json().get("refresh")
        self.instance2.is_active = False
        self.instance2.save()

    def test_auth_create_success(self):
        response = self.client.post(self.urls["auth-create"], {"phone": self.phone1, "password": self.password})
        self.assertEqual(response.status_code, 200)

    def test_auth_refresh_success(self):
        response = self.client.post(self.urls["auth-refresh"], {"refresh": self.refresh1})
        self.assertEqual(response.status_code, 200)

    def test_auth_verify_success(self):
        response = self.client.post(self.urls["auth-verify"], {"token": self.refresh1})
        self.assertEqual(response.status_code, 200)

    def test_auth_create_fail(self):
        response = self.client.post(self.urls["auth-create"], {"phone": self.phone2, "password": self.password})
        self.assertEqual(response.status_code, 401)

    def test_auth_refresh_fail(self):
        response = self.client.post(self.urls["auth-refresh"], {"refresh": self.refresh2})
        self.assertEqual(response.status_code, 401)

    def test_auth_verify_faila(self):
        response = self.client.post(self.urls["auth-verify"], {"token": self.refresh2})
        self.assertEqual(response.status_code, 401)
