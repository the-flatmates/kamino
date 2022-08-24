from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=200)
    elo = models.FloatField(default=1600)
    games_played = models.PositiveIntegerField(default=0)
    games_won = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.elo})"
