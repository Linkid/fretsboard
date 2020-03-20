from django.contrib import admin

from scoreboard.models import Player
from scoreboard.models import Score
from scoreboard.models import Song


class SongAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'artist', 'verified')
    list_filter = ('verified',)
    search_fields = ['title', 'artist']


admin.site.register(Player)
admin.site.register(Score)
admin.site.register(Song, SongAdmin)
