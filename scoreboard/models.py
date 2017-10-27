from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _


class Song(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    artist = models.CharField(verbose_name=_("Artist"), max_length=100, blank=True)
    year = models.IntegerField(verbose_name=_("Year"), blank=True, null=True)

    class Meta:
        ordering = ['slug']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.slug


class Player(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100, unique=True)

    def __str__(self, *args, **kwargs):
        return self.name

    def get_total_score(self):
        """Sum all scores for the player"""
        scores = self.score_set.all()
        return sum(i.score for i in scores)

    def get_medals(self):
        """Get number of each medal"""
        gold_medals = 0
        silver_medals = 0
        bronze_medals = 0

        # get all scores for the player
        my_scores = self.score_set.all()
        for my_score in my_scores:
            # get all scores for the song and difficulty
            all_scores = Score.objects.filter(song=my_score.song, difficulty=my_score.difficulty)
            # get best scores
            medals = all_scores.order_by('-score')

            if medals and medals[0].player == self:
                gold_medals += 1
            if medals.count() >= 2 and medals[1].player == self:
                silver_medals += 1
            if medals.count() >= 3 and medals[2].player == self:
                bronze_medals += 1

        return (gold_medals, silver_medals, bronze_medals)

    def get_gold_medals(self):
        """Get number of gold medals"""
        return self.get_medals()[0]

    def get_silver_medals(self):
        """Get number of silver medals"""
        return self.get_medals()[1]

    def get_bronze_medals(self):
        """Get number of bronze medals"""
        return self.get_medals()[2]


class Score(models.Model):
    DIFFICULTIES = (
        ("easy", _("Easy")),
        ("medium", _("Medium")),
        ("amazing", _("Amazing")),
    )
    MAX_STARS = 5

    song = models.ForeignKey(Song, verbose_name=_("Song"))
    player = models.ForeignKey(Player, verbose_name=_("Player"))
    difficulty = models.CharField(verbose_name=_("Difficulty"), choices=DIFFICULTIES, max_length=15)
    score = models.IntegerField(verbose_name=_("Score"))
    stars = models.IntegerField(verbose_name=_("Stars"))
    date = models.DateTimeField(verbose_name=_("Date"))

    class Meta:
        unique_together = ('song', 'player', 'difficulty')

    def __str__(self, *args, **kwargs):
        msg = "%(song)s (%(difficulty)s): %(player)s - %(score)d (%(date)s)"
        dico = {
            'song': self.song.title,
            'difficulty': self.difficulty,
            'player': self.player,
            'score': self.score,
            'date': self.date,
        }
        return msg % dico

    def stars_state(self):
        """Return a list of boolean representing the state of stars"""
        return [True] * self.stars + [False] * (self.MAX_STARS - self.stars)
