from django.urls import path, re_path
from . import views
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/video/(?P<video_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]

urlpatterns = [
    path('ws/video/<int:video_id>/', consumers.ChatConsumer.as_asgi(), name='chat'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
]
