from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TableConnection(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'table',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'table',
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            'table',
            {
                'type': 'message',
                'content': {'message': message}
            }
        )

    # Receive message from room group
    async def message(self, event):
        print(event)
        message = event['content']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))