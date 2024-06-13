
from django.db import models
from django.conf import settings
from videos.models import Video

class Message(models.Model):
    video = models.ForeignKey(Video, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    guest_id = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
