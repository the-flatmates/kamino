from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=200)
    elo = models.FloatField(default=1600)

    def __str__(self):
        return f"{self.name} ({self.elo})"
