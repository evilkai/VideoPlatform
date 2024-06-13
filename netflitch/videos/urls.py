from django.urls import path
from .views import upload_video, video_detail, videos

urlpatterns = [
    path('upload/', upload_video, name='upload_video'),
    path('video/<int:video_id>/', video_detail, name='video_detail'),
    path('videos/', videos, name='videos'),
]
