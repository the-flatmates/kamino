from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from bokeh.plotting import figure
from bokeh.embed import components

from .models import Player
from games.models import Game, Color

# def index(request):
#     player_list = Player.objects.order_by('-elo')
#     context = {"player_list": player_list}
#     return render(request, 'players/index.html', context)


def index(request):
 
   #create a plot
    plot = figure(plot_width=400, plot_height=400)
 
   # add a circle renderer with a size, color, and alpha
 
    plot.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
 
    script, div = components(plot)
    context = {'script': script, 'div': div}

    player_list = Player.objects.order_by('-elo')
    context["player_list"] = player_list
 
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

        red_games_won = red_games.filter(winners=Color.RED)
        blue_games_won = blue_games.filter(winners=Color.BLUE)

        games_won = red_games_won | blue_games_won
        games_won = games_won.order_by('-datetime')

        data["games"] = games
        data["games_won"] = games_won

        return data