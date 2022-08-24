from django.http import HttpResponse
from django.shortcuts import render

from .models import Player

def index(request):
    player_list = Player.objects.order_by('-elo')
    context = {"player_list": player_list}
    return render(request, 'players/index.html', context)

def player(request, player_name):
    players = Player.objects.filter(name=player_name)

    if len(players) != 1:
        return HttpResponse(f"{players}")

    named_player = players[0]    
    # output = ', '.join()
    return HttpResponse(f"{named_player}")