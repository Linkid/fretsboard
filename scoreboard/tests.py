from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from scoreboard.models import Player
from scoreboard.models import Score
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


class PlayerTestCase(TestCase):
    def setUp(self):
        # players
        self.player1 = Player.objects.create(name="Player1")
        self.player2 = Player.objects.create(name="Player2")
        self.player3 = Player.objects.create(name="Player3")
        self.player4 = Player.objects.create(name="Player4")
        self.player5 = Player.objects.create(name="Player5")
        # songs
        self.song1 = Song.objects.create(title="Song1", artist="Artist1", year=2017)
        self.song2 = Song.objects.create(title="Song2", artist="Artist2", year=2017)
        # scores
        Score.objects.create(
            song=self.song1,
            player=self.player1,
            difficulty="easy",
            score=100,
            stars=1,
            date=timezone.now()
        )
        Score.objects.create(
            song=self.song2,
            player=self.player1,
            difficulty="medium",
            score=200,
            stars=2,
            date=timezone.now()
        )
        Score.objects.create(
            song=self.song1,
            player=self.player2,
            difficulty="easy",
            score=200,
            stars=2,
            date=timezone.now()
        )
        Score.objects.create(
            song=self.song1,
            player=self.player3,
            difficulty="easy",
            score=300,
            stars=3,
            date=timezone.now()
        )
        Score.objects.create(
            song=self.song1,
            player=self.player4,
            difficulty="easy",
            score=400,
            stars=4,
            date=timezone.now()
        )

    def test_display_name(self):
        self.assertEquals(str(self.player1), self.player1.name)

    def test_get_total_score(self):
        total = 100 + 200
        self.assertEqual(self.player1.get_total_score(), total)
        self.assertEqual(self.player5.get_total_score(), 0)

    def test_get_gold_medals(self):
        gold_medals = 1
        self.assertEqual(self.player4.get_gold_medals(), gold_medals)

    def test_get_silver_medals(self):
        # player 3
        silver_medals = 1
        self.assertEqual(self.player3.get_silver_medals(), silver_medals)
        # player 4 (degraded state)
        silver_medals = 0
        self.assertEqual(self.player4.get_silver_medals(), silver_medals)

    def test_get_bronze_medals(self):
        bronze_medals = 1
        self.assertEqual(self.player2.get_bronze_medals(), bronze_medals)
