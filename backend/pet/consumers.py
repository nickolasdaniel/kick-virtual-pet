from channels.generic.websocket import AsyncJsonWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class PetConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket connect called")
        await self.channel_layer.group_add("pet_updates", self.channel_name)
        await self.accept()
        logger.info("WebSocket connection accepted")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("pet_updates", self.channel_name)
        logger.info("WebSocket disconnected")

    async def pet_update(self, event):
        try:
            logger.info("Broadcasting pet update: %s", event["data"])
            # This method is available on AsyncJsonWebsocketConsumer
            await self.send_json(event["data"])
        except Exception as e:
            logger.exception("Error sending pet update")
