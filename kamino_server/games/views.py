from django.shortcuts import render
from django.views import generic
from django.utils.dateparse import parse_datetime
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os

from .models import Game, Color
from players.models import Player
from .forms import GameForm, GameFinishedForm

from formtools.wizard.views import SessionWizardView

def index(request):
    game_list = Game.objects.order_by('-datetime')
    context = {"game_list": game_list}
    return render(request, 'games/index.html', context)


class GameView(generic.DetailView):
    model = Game

    def get_object(self, queryset=None):
        datetime_key = parse_datetime(self.kwargs['game_datetime'])
        return Game.objects.filter(datetime=datetime_key).first()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['winner_color'] = str(self.object.winners)

        elos = self.object.get_elo_dict()

        red_team_elos = {}
        blue_team_elos = {}
        for member in self.object.red_team.all():
            name = member.name
            red_team_elos[name] = elos[name]
        for member in self.object.blue_team.all():
            name = member.name
            blue_team_elos[name] = elos[name]

        data["red_team_elos"] = red_team_elos
        data["blue_team_elos"] = blue_team_elos

        return data


def calculate_elos(winners: list[Player], losers: list[Player]):
    # TODO: more complex function
    new_elos = {}

    for winner in winners:
        new_elos[winner.name] = winner.elo + 1
    
    for loser in losers:
        new_elos[loser.name] = loser.elo - 1

    return new_elos


def update_elos(new_elos: dict[str, float]):
    for name, elo in new_elos.items():
        Player.objects.get(name=name).update(elo=elo)


# class SubmitGame(generic.edit.CreateView):
#     model = Game
#     fields = ['datetime', 'red_team', 'blue_team', 'winners', 'board_image']

#     success_url = "games/submit_game_finished"

#     def save(self, *args, **kwargs):
#         game = self.cleaned_data

#         hidtorical_elos = {}
#         for player in game.red_team + game.blue_team:
#             historical_elos[player.name] = player.elo
#         elos = json.dumps(historical_elos)
        
#         if game.winners == Color.RED:
#             winning_team = game.red_team
#             losing_team = game.blue_team
#         else:
#             winning_team = game.blue_team
#             losing_team = game.red_team

#         update_elos(calculate_elos(winning_team, losing_team))

#         game.save()
#         return game


class GameWizard(SessionWizardView):
    # TODO: Add processing of board image after first form, 
    # so second form can display analysis for human correction
    form_list = [GameForm, GameFinishedForm]

    file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

    template_name = "games/game_form.html"

    def done(self, form_list, **kwargs):
        print(form_list)

        game = self.cleaned_data

        hidtorical_elos = {}
        for player in game.red_team + game.blue_team:
            historical_elos[player.name] = player.elo
        elos = json.dumps(historical_elos)
        
        if game.winners == Color.RED:
            winning_team = game.red_team
            losing_team = game.blue_team
        else:
            winning_team = game.blue_team
            losing_team = game.red_team

        update_elos(calculate_elos(winning_team, losing_team))

        return HttpResponseRedirect('games/')
