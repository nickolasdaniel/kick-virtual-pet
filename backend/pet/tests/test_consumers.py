# backend/pet/tests/test_consumers.py
from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
from asgiref.sync import async_to_sync
from kick_virtual_pet.asgi import application

class PetConsumerTest(TransactionTestCase):
    def test_websocket_receives_update(self):
        # Create a communicator to simulate a WebSocket connection.
        communicator = WebsocketCommunicator(application, "/ws/pet/")
        connected, _ = async_to_sync(communicator.connect)()
        self.assertTrue(connected)
        
        # Prepare test data to simulate a pet update.
        test_data = {
            "name": "TestPet",
            "hunger": 40,
            "energy": 60,
            "happiness": 60,
            "health": 100,
            "mood": "evolved"
        }
        
        # Simulate sending a "pet_update" event from the channel layer.
        async_to_sync(communicator.send_json_to)({
            "type": "pet_update",
            "data": test_data
        })
        
        # Receive the JSON data from the consumer.
        response = async_to_sync(communicator.receive_json_from)()
        self.assertEqual(response, test_data)
        
        # Close the connection.
        async_to_sync(communicator.disconnect)()
