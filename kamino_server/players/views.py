from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from bokeh.plotting import figure
from bokeh.embed import components

import numpy as np

from .models import Player
from games.models import Game, Color

def get_player_games(player: Player):
    red_games = Game.objects.filter(red_team=player)
    blue_games = Game.objects.filter(blue_team=player)

    games = red_games | blue_games

    return games


def get_elos(name: str, games):
    elos = []
    for game in games:
        elo_dict = game.get_elo_dict()
        if name in elo_dict:
            elos.append(elo_dict[name])
    
    return elos


def make_plot(title, hist, edges):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)

    p.xaxis.axis_label = 'Elo'
    p.grid.grid_line_color="white"
    return p


def elo_distribution(player_list):
    elo_list = [player.elo for player in player_list]
    hist, edges = np.histogram(elo_list, density=True, bins=50)

    return make_plot(None, hist, edges)


def index(request):
    context = {}

    #create a plot
    plot = figure(plot_width=400, plot_height=400)

    player_list = Player.objects.order_by('-elo')
    context["player_list"] = player_list

    max_games = 0
    historical_elos = {}
    for player in player_list:
        player_games = get_player_games(player).order_by("datetime")
        historical_elo = get_elos(player.name, player_games)

        if len(historical_elo) > max_games:
            max_games = len(historical_elo)
        historical_elos[player.name] = historical_elo
    
    x_range = range(max_games)

    for name, elo in historical_elos.items():
        plot.line(x_range, elo, legend_label=name, line_width=2)
    
    script, div = components(plot)
    context['hist_elo_script'] = script
    context['hist_elo_div'] = div

    script, div = components(elo_distribution(player_list))
    context['elo_dist_script'] = script
    context['elo_dist_div'] = div
 
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