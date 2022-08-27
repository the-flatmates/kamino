from django.shortcuts import render

from .models import Game

def index(request):
    game_list = Game.objects.order_by('-datetime')
    context = {"game_list": game_list}
    return render(request, 'games/index.html', context)


def game(request, game_datetime):
    games = Game.objects.filter(datetime=game_datetime)

    if len(games) != 1:
        return HttpResponse(f"{games}")

    specific_game = games[0]

    context = { 
        "datetime": specific_game.datetime,
        "red_team": specific_game.red_team.all(),
        "blue_team": specific_game.blue_team.all(),
        "winners": specific_game.winners,
        "board": specific_game.board,
    }

    return render(request, 'games/detailed_game.html', context)
