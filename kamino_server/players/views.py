from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Player
from games.models import Game

def index(request):
    player_list = Player.objects.order_by('-elo')
    context = {"player_list": player_list}
    return render(request, 'players/index.html', context)


class PlayerView(generic.DetailView):
    model = Player

    def get_object(self, queryset=None):
        return Player.objects.filter(name=self.kwargs['name']).first()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        red_games = Game.objects.filter(red_team=self.object)
        blue_games = Game.objects.filter(blue_team=self.object)

        games = red_games | blue_games
        games = games.order_by('-datetime')

        data["games"] = games

        return data