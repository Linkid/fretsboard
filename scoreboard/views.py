from django.views import generic

from scoreboard.models import Song


class Songs(generic.ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'scoreboard/songs.html'
    paginate_by = 20
