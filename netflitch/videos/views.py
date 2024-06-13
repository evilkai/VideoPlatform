from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Video
from .tasks import notify_subscribers

@login_required
def upload_video(request):
    if request.method == 'POST':
        video = Video.objects.create(
            channel=request.user.channel,
            title=request.POST['title'],
            description=request.POST['description'],
            file=request.FILES['file']
        )
        notify_subscribers.delay(video.id)
        return redirect('home')
    return render(request, 'videos/upload.html')

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'videos/video_detail.html', {'video': video})


def videos(request):
    videos = Video.objects.all()
    return render(request, 'videos/videos.html', {'videos': videos})
