import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from ..models import GroupModel
from django.db.models import Q


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self._add_groups(await self._get_user_groups())
        await self.accept()

    async def disconnect(self, close_code):
        await self._remove_groups(await self._get_user_groups())

    async def receive(self, text_data):
        try:
            text_data_json = self._get_data(text_data)
            message = text_data_json.get("data", None).get("message", None)
            await self.send(text_data=json.dumps({"status": True, "data": {"message": message}}))
        except Exception as e:
            await self.send(text_data=json.dumps({"status": False, "data": {"error": str(e)}}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"status": event.get("status", True), "data": {
            "result": event.get("data", None),
            "action": event.get("action", None)
        }}))

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
        user = self.scope.get("user")
        groups = GroupModel.objects.filter(
            Q(is_public=True) | Q(users=user) if user and user.is_authenticated else Q(is_public=True)
        ).values_list("id", flat=True)
        return [f"group_{i}" for i in groups] + ([user.username] if user and user.is_authenticated else [])
