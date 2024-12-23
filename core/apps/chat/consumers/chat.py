import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import logging

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            return await self.close()
        await self._add_groups(await self._get_user_groups())
        await self.accept()

    async def disconnect(self, close_code):
        await self._remove_groups(await self._get_user_groups())

    async def receive(self, text_data):
        text_data_json = self._get_data(text_data)
        message = text_data_json.get("message", None)
        await self.channel_layer.group_send("group_1", {"type": "chat_message", "message": message})

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    def _get_data(self, text_data) -> dict:
        try:
            return json.loads(text_data)
        except json.JSONDecodeError:
            return {}

    async def _add_groups(self, groups):
        for group in groups:
            await self.channel_layer.group_add(group, self.channel_name)

    async def _remove_groups(self, groups):
        for group in groups:
            await self.channel_layer.group_discard(group, self.channel_name)

    @sync_to_async
    def _get_user_groups(self) -> list:
        groups = ["group_%s" % i for i in list(self.scope["user"].chats.values_list("id", flat=True))]
        groups.append(self.scope["user"].username)
        return groups
