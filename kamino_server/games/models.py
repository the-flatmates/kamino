from django.db import models

from typing import List

import json

from players.models import Player


class Color(models.TextChoices):
    RED = "RED", "RED"
    BLUE = "BLUE", "BLUE"

    # def __str__(self):
    #     return f"{self.value}"


class Word(models.Model):
    word = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.word}"
    

class CardMetaData(models.Field):
    guessed_by = models.CharField(
        max_length=5,
        choices=Color.choices,
        default=Color.RED,
    )
    turn_guessed = models.PositiveIntegerField()

    def db_type(self, connection):
        return 'cardmetadata'


class Card(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    metadata = CardMetaData(null=True)


class BoardField(models.Field):
    red_words = models.ManyToManyField(Card, related_name='red_words')
    blue_words = models.ManyToManyField(Card, related_name='blue_words')
    neutral_words = models.ManyToManyField(Card, related_name='neutral_words')
    bomb = models.OneToOneField(Card, on_delete=models.CASCADE)

    def db_type(self, connection):
        return 'board'


class Game(models.Model):
    datetime = models.DateTimeField('date played')

    red_team = models.ManyToManyField(Player, related_name='red_team')
    blue_team = models.ManyToManyField(Player, related_name='blue_team')

    elos = models.JSONField(null=True)

    winners = models.CharField(
        max_length=5,
        choices=Color.choices,
        default=Color.RED,
    )

    board = BoardField(null=True)

    def __str__(self):
        return f"{self.datetime} ({self.winners})"

    def get_elo_dict(self):
        try:
            # for some reason elos is getting single quotes
            return json.loads(json.dumps(self.elos))
        except:
            return ""