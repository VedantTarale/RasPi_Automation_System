from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/reading/', consumers.ReadingConsumer.as_asgi())
]