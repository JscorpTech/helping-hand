import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from django.db.models import Q

import logging
from ..models import GroupModel
from ..serializers import CallSerializer
from ..services import ChatService

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            cache.set("channel_%s" % user.username, self.channel_name, 60 * 60 * 24)
        
        groups = await self._get_user_groups()
        logger.info(f"WS CONNECT: User {user} joined groups: {groups}")
        await self._add_groups(groups)
        await self.accept()

    async def disconnect(self, close_code):
        await self._remove_groups(await self._get_user_groups())

    async def receive(self, text_data):
        try:
            if self.scope["user"].is_anonymous:
                return await self.send(text_data=json.dumps({"status": False, "detail": "Unauthorized"}))
            data = self._get_data(text_data)
            service = ChatService(context={"user": self.scope["user"]})
            serializer = CallSerializer(data=data)
            if not serializer.is_valid():
                return await self.send(text_data=json.dumps({"status": False, "data": serializer.errors}))
            response = service.process(serializer.validated_data)
            # Direct response for testing
            await self.send(text_data=json.dumps({"status": True, "data": response["data"], "action": "direct_response"}))
            
            logger.info(f"WS SEND: User {self.scope['user']} sending to group {response['group']}")
            await self.channel_layer.group_send(
                response["group"], {"type": "chat_message", "status": True, "data": response["data"], "action": "call"}
            )
        except Exception as e:
            logger.error(f"WS ERROR in receive: {e}", exc_info=True)
            await self.send(text_data=json.dumps({"status": False, "detail": str(e)}))

    async def chat_message(self, event):
        logger.info(f"WS RECEIVE: chat_message in {self.channel_name} for user {self.scope.get('user')}")
        await self.send(
            text_data=json.dumps(
                {
                    "status": event.get("status", True),
                    "data": {"result": event.get("data", None), "action": event.get("action", None)},
                }
            )
        )

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
