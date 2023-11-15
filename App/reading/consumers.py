from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
# from django.core.serializers import serialize

class ReadingConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "test_consumer_group"

        async_to_sync (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status': "connected"}))

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data=text_data)

    def disconnect(self, code):
        return super().disconnect(code)

    def send_update(self,event):
        self.send(json.dumps(event['value']))
