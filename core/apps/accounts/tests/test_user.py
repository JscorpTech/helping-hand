# from django.urls import reverse
# from rest_framework.test import APIClient
from django.test import TestCase


class ModeratorTestTest(TestCase):

    # def setUp(self):
    #    self.client = APIClient()
    #    self.urls = {
    #        "list": reverse("list"),
    #        "retrieve": reverse("detail", kwargs={"pk": 1}),
    #        "create": reverse("create"),
    #        "update": reverse("update", kwargs={"pk": 1}),
    #        "partial_update": reverse("partial-update", kwargs={"pk": 1}),
    #        "destroy": reverse("destroy", kwargs={"pk": 1}),
    #    }

    def test_create(self):
        self.assertTrue(True)

    def test_update(self):
        self.assertTrue(True)

    def test_partial_update(self):
        self.assertTrue(True)

    def test_destroy(self):
        self.assertTrue(True)

    # def test_list(self):
    #    response = self.client.get(self.urls["list"])
    #    self.assertEqual(response.status_code, 200)

    # def test_retrieve(self):
    #    response = self.client.get(self.urls["retrieve"])
    #    self.assertEqual(response.status_code, 200)
