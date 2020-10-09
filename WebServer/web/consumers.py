from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import *


class TableConnection(WebsocketConsumer):
    def connect(self):

        async_to_sync(self.channel_layer.group_add)(
            'table',
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'table',
            self.channel_name
        )

    def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        action = message['action']

        if action == 'save_data':
            extension = Extension.objects.get(extension_name=message['extension_name'])
            SavedData.objects.create(extension=extension, field_name=message['field_name'],
                                     content=json.dumps(message['content']))


    # Receive message from room group
    def message(self, event):
        print(event)
        message = event['content']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))