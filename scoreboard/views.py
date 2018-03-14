import binascii
import hashlib
import operator
from functools import reduce

import cerealizer
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import escape
from django.views import generic

from scoreboard.models import Player
from scoreboard.models import Score
from scoreboard.models import Song


class Songs(generic.ListView):
    """
    List all songs
    """
    model = Song
    context_object_name = 'songs'
    template_name = 'scoreboard/songs.html'
    paginate_by = 15

    def get_queryset(self, *args, **kwargs):
        """
        Display songs filtered by the search query
        """
        result = super().get_queryset(*args, **kwargs)

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(artist__icontains=q) for q in query_list))
            )

        return result


def song(request, song_id):
    """
    Song scores
    """
    song = get_object_or_404(Song, slug=song_id)
    return render(request, 'scoreboard/song.html', {'song': song})


class Players(generic.ListView):
    """
    List all players
    """
    model = Player
    context_object_name = 'players'
    template_name = 'scoreboard/players.html'
    paginate_by = 15

    def get_queryset(self, *args, **kwargs):
        """
        Display players filtered by the search query
        """
        result = super().get_queryset(*args, **kwargs)

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(name__icontains=q) for q in query_list)),
            )

        return result


def player(request, player_name):
    """
    Player info
    """
    player = get_object_or_404(Player, name=player_name)
    positions = dict()  # will contain { song: { difficulty: { score: position } } }

    # get all played songs (in Score objects)
    scores_player = player.score_set.order_by('song').only('song').distinct()
    for score_player in scores_player:
        song = score_player.song
        positions[song] = dict()  # will contain { difficutly: { score: position } }
        # get all scores for the song
        scores_song = Score.objects.filter(song=song)
        # get difficulties
        scores_song_player = scores_song.filter(player=player).order_by('-difficulty').only('difficulty').distinct()
        for score_song_player in scores_song_player:
            difficulty = score_song_player.difficulty
            difficulty_val = score_song_player.get_difficulty_display()
            # get all scores for the song and the difficulty
            scores = scores_song.filter(difficulty=difficulty).order_by('-score')
            # get all scores for the song, the difficulty and the player
            player_scores = scores.filter(player=player).order_by('-score')
            # get positions
            player_positions = {score: list(scores).index(score) + 1 for score in player_scores}

            # save positions
            positions[song][difficulty_val] = player_positions  # contains { score: position }

    return render(request, 'scoreboard/player.html', {'player': player, 'positions': positions})


def scoreboard(request):
    """
    Scoreboard summary
    """
    players = Player.objects.all()
    scores = Score.objects.all()
    songs = Song.objects.all()

    context = {
        'players': players,
        'scores': scores,
        'songs': songs,
    }

    return render(request, 'scoreboard/scoreboard.html', context)


class Search(generic.RedirectView):
    """
    Search in models. Redirect to the scoreboard if no models found.
    """
    query_string = True

    def get(self, request, *args, **kwargs):
        obj = request.GET.get('obj', 'songs')
        if obj in ['songs', 'players']:
            self.pattern_name = obj
        else:
            self.pattern_name = 'scoreboard'

        return super().get(request, *args, **kwargs)


def add_score(request):
    """
    Add a score for a player and a song

    Returns a binary HttpResponse.
    """
    # scores_to_insert = list()

    # get GET params
    song_title = escape(request.GET.get('songName', None))
    song_hash = escape(request.GET.get('songHash', None))
    song_instrument = escape(request.GET.get('songPart', None))
    scores = escape(request.GET.get('scores', None))
    version = escape(request.GET.get('version', None))
    timestamp = escape(request.GET.get("timestamp", timezone.now()))
    remote_addr = request.META.get("REMOTE_ADDR", None)

    # check params
    if song_title is None or scores is None:
        return HttpResponse(False)

    # decode scores
    try:
        scores_decoded = cerealizer.loads(binascii.unhexlify(scores))
    except ValueError:
        return HttpResponse(False)

    # find the song or create it
    song, created_song = Song.objects.get_or_create(
        title=song_title,
        notes=song_hash,
    )

    # get scores items
    for difficulty_id, scores_items in scores_decoded.items():
        for score, stars, name, hash_score in scores_items:
            # check the hash
            hash_str = "%d%d%d%s" % (difficulty_id, score, stars, name)
            hash_bytes = bytes(hash_str, 'utf-8')
            hash_sha = hashlib.sha1(hash_bytes).hexdigest()
            if hash_score != hash_sha:
                continue

            # check stars number
            if stars < 0 or stars > Score.MAX_STARS:
                continue

            # check the difficulty
            if difficulty_id < 0 or difficulty_id >= len(Score.DIFFICULTIES):
                continue
            difficulty = Score.DIFFICULTIES[difficulty_id][0]

            # add scores to the list
            # scores_to_insert.append((difficulty, score, stars, name))

            # find the player or create it
            player, created_player = Player.objects.get_or_create(
                name=name,
            )
            player.remote_address = remote_addr
            player.save()

            # write scores
            try:
                Score.objects.update_or_create(
                    song=song,
                    player=player,
                    difficulty=difficulty,
                    score=score,
                    stars=stars,
                    date=timestamp,
                    version=version,
                    instrument=song_instrument,
                )
            except IntegrityError:
                return HttpResponse(False)

    return HttpResponse(True)
