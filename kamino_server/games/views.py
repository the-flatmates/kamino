from django.shortcuts import render

from .models import Game

def index(request):
    # player_list = Player.objects.order_by('-elo')
    # context = {"player_list": player_list}
    return render(request, 'players/index.html', "Temp")
