from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from config.asgi import application

from ..models import GroupModel


class WebSocketTest(TestCase):

    async def _connect(self):
        communicator = WebsocketCommunicator(application, "ws/chat/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        return communicator

    async def test_retrieve(self):
        communicator = await self._connect()
        await communicator.send_json_to({"data": {"message": "Test Message"}})
        response = await communicator.receive_json_from()
        self.assertEqual(response["status"], False)

    async def test_send_message(self):
        client = APIClient()
        group, user = await self._create_fake()
        await sync_to_async(client.force_authenticate)(user)
        response = await sync_to_async(client.post)(
            reverse("group-send-message", kwargs={"pk": group.pk}),
            {"text": "salom"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["status"])

    @sync_to_async
    def _create_fake(self):
        return GroupModel._create_fake(), get_user_model()._create_fake()
