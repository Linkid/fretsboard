from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import generic

from scoreboard.models import Player
from scoreboard.models import Song


class Songs(generic.ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'scoreboard/songs.html'
    paginate_by = 20


def song(request, song_id):
    """
    Song scores
    """
    song = get_object_or_404(Song, slug=song_id)
    return render(request, 'scoreboard/song.html', { 'song': song })


class Players(generic.ListView):
    model = Player
    context_object_name = 'players'
    template_name = 'scoreboard/players.html'
    paginate_by = 20
