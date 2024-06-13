
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from .models import Channel, Subscription
from .forms import ChannelForm
from videos.forms import VideoUploadForm
from videos.models import Video
from django.conf import settings
from videos.forms import VideoUploadForm, VideoEditForm

from django.core.cache import cache

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    next_page = 'profile'

def logout_view(request):
    auth_logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Channel.objects.create(user=user)
            auth_login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
@cache_page(settings.CACHE_TTL)
def profile(request):
    channel, created = Channel.objects.get_or_create(user=request.user)  # Получение или создание канала
    if request.method == 'POST':
        form = ChannelForm(request.POST, request.FILES, instance=channel)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ChannelForm(instance=channel)
    return render(request, 'users/profile.html', {'form': form})



def get_videos(channel):
    cache_key = f'videos_{channel.id}'
    videos = cache.get(cache_key)
    if not videos:
        videos = Video.objects.filter(channel=channel)
        cache.set(cache_key, videos, settings.CACHE_TTL)
    return videos


# @cache_page(settings.CACHE_TTL)
def channel_view(request, channel_id):
    cache_key = f'channel_videos_{channel_id}'
    # videos = cache.get(cache_key)
    videos = Video.objects.filter(channel= channel_id)
    if not videos:
        channel = get_object_or_404(Channel, id=channel_id)
        videos = Video.objects.filter(channel=channel)
        cache.set(cache_key, videos, timeout=settings.CACHE_TTL)
    else:
        channel = Channel.objects.get(id=channel_id)

    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(user=request.user, channel=channel).exists()
    return render(request, 'users/channel.html', {
        'channel': channel,
        'videos': videos,
        'is_subscribed': is_subscribed,
        'subscriber_count': channel.subscriber_count
    })


@login_required
# @cache_page(settings.CACHE_TTL)
@csrf_protect
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.channel = request.user.channel
            video.save()
            return redirect('profile')
    else:
        form = VideoUploadForm()
    return render(request, 'videos/upload.html', {'form': form})


@login_required
@csrf_protect
def edit_video(request):
    if request.method == 'POST':
        form = VideoEditForm(request.POST)
        if form.is_valid():
            video_id = form.cleaned_data['video_id']
            video = get_object_or_404(Video, id=video_id, channel=request.user.channel)
            video.title = form.cleaned_data['title']
            video.description = form.cleaned_data['description']
            video.save()
            return redirect('channel_view', channel_id=request.user.channel.id)
    return redirect('home')


@login_required
@csrf_protect
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id, channel=request.user.channel)
    video.delete()
    return redirect('channel_view', channel_id=request.user.channel.id)



@login_required
def subscribe(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)
    Subscription.objects.get_or_create(user=request.user, channel=channel)
    return redirect('channel_view', channel_id=channel_id)

@login_required
def unsubscribe(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)
    subscription = Subscription.objects.filter(user=request.user, channel=channel)
    if subscription.exists():
        subscription.delete()
    return redirect('channel_view', channel_id=channel_id)



@cache_page(settings.CACHE_TTL)
def home(request):
    return render(request, 'home.html')
