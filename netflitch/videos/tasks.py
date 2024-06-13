from celery import shared_task
from .models import Video, Notification

@shared_task
def notify_subscribers(video_id):
    video = Video.objects.get(id=video_id)
    subscribers = video.channel.subscribers.all()
    for subscriber in subscribers:
        Notification.objects.create(user=subscriber, video=video)
