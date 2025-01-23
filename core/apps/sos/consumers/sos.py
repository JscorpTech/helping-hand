from channels.generic.websocket import AsyncWebsocketConsumer
import logging  # noqa
import json


class SosConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "user_%s" % self.scope["url_route"]["kwargs"]["room_name"]
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def position(self, event):
        await self.send(text_data=json.dumps(event))

    async def receive(self, text_data): ...
