from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _


class Song(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    artist = models.CharField(verbose_name=_("Artist"), max_length=100)
    year = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.slug


class Player(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100, unique=True)

    def __str__(self, *args, **kwargs):
        return self.name


class Score(models.Model):
    DIFFICULTIES = (
        ("easy", _("Easy")),
        ("medium", _("Medium")),
        ("amazing", _("Amazing")),
    )

    song = models.ForeignKey(Song)
    player = models.ForeignKey(Player)
    difficulty = models.CharField(verbose_name=_("Difficulty"), choices=DIFFICULTIES, max_length=15)
    score = models.IntegerField()
    stars = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self, *args, **kwargs):
        msg = "%(song)s (%(difficulty)s): %(player)s - %(score)d (%(date)s)"
        dico = {
            'song': self.song,
            'difficulty': self.difficulty,
            'player': self.player,
            'score': self.score,
            'date': self.date,
        }
        return msg % dico
