# backend/pet/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PetConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add this connection to the "pet_updates" group.
        await self.channel_layer.group_add("pet_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove from the group.
        await self.channel_layer.group_discard("pet_updates", self.channel_name)

    # Receive messages from the group.
    async def pet_update(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))
