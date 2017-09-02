from django.conf.urls import url

from scoreboard import views


urlpatterns = [
    # songs
    url(r'^songs/$', views.Songs.as_view(), name='songs'),
    url(r'^songs/(?P<song_id>.+)/$', views.song, name='song'),
    # players
    url(r'^players/$', views.Players.as_view(), name='players'),
]
