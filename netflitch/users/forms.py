from django import forms
from .models import Channel, Subscription
from videos.models import Video


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['avatar', 'description']
