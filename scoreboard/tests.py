from django.test import TestCase
from django.utils.text import slugify

from scoreboard.models import Song


class SongTestCase(TestCase):
    def test_generated_slug(self):
        song_title = "This is a long Song title"
        song_slug = slugify(song_title)
        song = Song.objects.create(title=song_title, artist="Artist1", year=2017)
        self.assertEqual(song.slug, song_slug)

    def test_display_slug(self):
        song = Song.objects.create(title="This is a long Song title", artist="Artist1", year=2017)
        self.assertEqual(str(song), song.slug)
