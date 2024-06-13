from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Channel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    @property
    def subscriber_count(self):
        return self.subscribers.count()

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='subscribers')

    class Meta:
        unique_together = ('user', 'channel')
