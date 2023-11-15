from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
# from django.core.serializers import serialize

class ReadingConsumer(WebsocketConsumer):
    
    
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({'status': "connected"}))

    def receive(self, text_data=None, bytes_data=None):
        # queryset = Reading.objects.all()
        # serialized_data = serialize('json', queryset)
        self.send(text_data=text_data)

    def disconnect(self, code):
        return super().disconnect(code)
    
