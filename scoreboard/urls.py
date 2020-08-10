from django.conf.urls import re_path

from scoreboard import views


urlpatterns = [
    re_path(r'^$', views.scoreboard, name='scoreboard'),
    re_path(r'^search$', views.Search.as_view(), name='search'),
    # songs
    re_path(r'^songs/$', views.Songs.as_view(), name='songs'),
    re_path(r'^songs/(?P<song_id>.+)/$', views.song, name='song'),
    # players
    re_path(r'^players/$', views.Players.as_view(), name='players'),
    re_path(r'^players/(?P<player_name>.+)$', views.player, name='player'),
    # upload
    re_path(r'^upload$', views.add_score, name='add_score'),
]
