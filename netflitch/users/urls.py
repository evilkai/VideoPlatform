from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, profile, channel_view, edit_video, delete_video

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('channel/<int:channel_id>/', channel_view, name='channel_view'),
    path('edit_video/', edit_video, name='edit_video'),
    path('delete_video/<int:video_id>/', delete_video, name='delete_video'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)