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
    name = models.CharField(verbose_name=_("Name"), max_length=100)

    def __str__(self, *args, **kwargs):
        return self.name
