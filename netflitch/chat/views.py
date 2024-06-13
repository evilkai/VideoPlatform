from django.shortcuts import render, get_object_or_404
from videos.models import Video
from .models import Message

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    messages = Message.objects.filter(video=video).order_by('timestamp')
    return render(request, 'videos/video_detail.html', {
        'video': video,
        'messages': messages,
    })
