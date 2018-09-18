import binascii

import cerealizer
from django.db import IntegrityError
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
        self.song1 = Song.objects.create(title="Song1", artist="Artist1", year=2017, verified=True)
        self.song2 = Song.objects.create(title="Song2", artist="Artist2", year=2017, verified=True)
        self.song3 = Song.objects.create(title="Song3", artist="Artist3", year=2017, verified=False)
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
            song=self.song3,
            player=self.player1,
            difficulty="medium",
            score=800,
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
        self.assertEqual(str(self.player1), self.player1.name)

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


class ScoreTestCase(TestCase):
    def setUp(self):
        # players
        self.player1 = Player.objects.create(name="Player1")
        self.player2 = Player.objects.create(name="Player2")
        # songs
        self.song1 = Song.objects.create(title="Song1", artist="Artist1", year=2017)
        self.song2 = Song.objects.create(title="Song2", artist="Artist2", year=2017)
        # scores
        self.score = Score.objects.create(
            song=self.song1,
            player=self.player1,
            difficulty="easy",
            score=100,
            stars=1,
            date=timezone.now()
        )

    def test_unicity_ok(self):
        score_song = Score.objects.create(
            song=self.song2,
            player=self.player1,
            difficulty="easy",
            score=100,
            stars=1,
            date=timezone.now()
        )
        self.assertIn(score_song, Score.objects.all())

        score_player = Score.objects.create(
            song=self.song1,
            player=self.player2,
            difficulty="easy",
            score=100,
            stars=1,
            date=timezone.now()
        )
        self.assertIn(score_player, Score.objects.all())

        score_difficulty = Score.objects.create(
            song=self.song1,
            player=self.player1,
            difficulty="medium",
            score=100,
            stars=1,
            date=timezone.now()
        )
        self.assertIn(score_difficulty, Score.objects.all())

    def test_unicity_ko(self):
        with self.assertRaises(IntegrityError):
            Score.objects.create(
                song=self.song1,
                player=self.player1,
                difficulty="easy",
                score=200,
                stars=2,
                date=timezone.now()
            )

    def test_display_score(self):
        expected_str_score = "Song1 (easy): Player1 - 100 (%s)" % self.score.date
        self.assertEqual(str(self.score), expected_str_score)

    def test_stars_state(self):
        actual_stars_state = self.score.stars_state()
        expected_stars_state = [True, False, False, False, False]

        self.assertEqual(len(actual_stars_state), len(expected_stars_state))
        self.assertListEqual(actual_stars_state, expected_stars_state)


class UploadTestCase(TestCase):
    def test_upload(self):
        score = {2: [(95908, 5, 'ball', 'ae023fbc6bf4a764fdba0423ea7bb801d80bde51')]}
        score_str = binascii.hexlify(cerealizer.dumps(score))
        # score_str = "63657265616c310a330a646963740a6c6973740a7475706c650a340a6939353930380a69350a75340a62616c6c7534300a61653032336662633662663461373634666462613034323365613762623830316438306264653531310a72310a69320a310a72320a72300a"

        attrs = {
            "songName": "Song title",
            "songHash": "dadacafe",
            "version": "4.0",
            "scores": score_str,
        }
        response = self.client.get('/upload', attrs)

        # check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"True")
        # check objects
        self.assertEqual(Score.objects.count(), 1)
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(Player.objects.count(), 1)
