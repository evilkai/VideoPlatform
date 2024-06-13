from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/video/<int:video_id>/', consumers.ChatConsumer.as_asgi()),
]
