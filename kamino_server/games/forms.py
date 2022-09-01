from django import forms
from django.db import models

from players.models import Player 
from .models import Color

from .widgets import ImagePreviewWidget


class GameForm(forms.Form):
    datetime = forms.CharField(widget=forms.TextInput(attrs={'type':'datetime-local'}))

    red_team = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    blue_team = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)

    board_image = forms.ImageField(widget=ImagePreviewWidget, required=True)

class GameFinishedForm(forms.Form):
    winners = forms.ChoiceField(choices=Color.choices, required=True)
    
    board_finished_image = forms.ImageField(widget=ImagePreviewWidget, required=True)
    board_key_image = forms.ImageField(widget=ImagePreviewWidget, required=True)