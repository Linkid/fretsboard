from django.conf.urls import url

from scoreboard import views


urlpatterns = [
    url(r'^$', views.scoreboard, name='scoreboard'),
    url(r'^search$', views.Search.as_view(), name='search'),
    # songs
    url(r'^songs/$', views.Songs.as_view(), name='songs'),
    url(r'^songs/(?P<song_id>.+)/$', views.song, name='song'),
    # players
    url(r'^players/$', views.Players.as_view(), name='players'),
    url(r'^players/(?P<player_name>.+)$', views.player, name='player'),
    # upload
    url(r'^upload$', views.add_score, name='add_score'),
]
