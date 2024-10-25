from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from a_users.views import profile_view
from django.conf import settings
from a_home.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('allauth.urls')),
    path('chat/', include('a_rtchat.urls')),
    path('profile/', include('a_users.urls')),
    path('@<username>/', profile_view, name="profile"),
    path('game/', include('a_game.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
