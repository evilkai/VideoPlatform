from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from videos import views as video_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('videos/', include('videos.urls')),
    path('', user_views.home, name='home'),
    path('login/', user_views.CustomLoginView.as_view(), name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('channel/<int:channel_id>/', user_views.channel_view, name='channel_view'),
    path('channel/<int:channel_id>/subscribe/', user_views.subscribe, name='subscribe'),
    path('channel/<int:channel_id>/unsubscribe/', user_views.unsubscribe, name='unsubscribe'),
    path('video/<int:video_id>/', video_views.video_detail, name='video_detail'),
    path('upload_video/', user_views.upload_video, name='upload_video'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)