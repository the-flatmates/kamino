from django.shortcuts import render

from .models import Game

def index(request):
    game_list = Game.objects.order_by('-datetime')
    context = {"game_list": game_list}
    return render(request, 'games/index.html', context)
