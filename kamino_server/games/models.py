from django.db import models

from players.models import Player


class Color(models.TextChoices):
    RED = "RED"
    BLUE = "BLUE"

class Card(models.Model):
    word = models.CharField(max_length=200)
    guessed_by = models.CharField(
        max_length=5,
        choices=Color.choices,
        default=Color.RED,
    )
    turn_guessed = models.PositiveIntegerField()

class Board(models.Model):
    red_words = models.ManyToManyField(Card)
    blue_words = models.ManyToManyField(Card)
    neutral_words = models.ManyToManyField(Card)
    bomb = models.ManyToManyField(Card)  

class Game(models.Model):
    datetime = models.DateTimeField('date played')
    red_team = models.ManyToManyField(Player)
    blue_team = models.ManyToManyField(Player)

    winners = models.ManyToManyField(Player)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
