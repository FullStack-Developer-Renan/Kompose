from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=255)

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    votes = models.IntegerField(default=1)

