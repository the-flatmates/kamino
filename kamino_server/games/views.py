from django.shortcuts import render
from django.views import generic
from django.utils.dateparse import parse_datetime

from .models import Game, Color

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


# def game(request, game_datetime):
#     games = Game.objects.filter(datetime=game_datetime)

#     if len(games) != 1:
#         return HttpResponse(f"{games}")

#     specific_game = games[0]

#     context = { 
#         "datetime": specific_game.datetime,
#         "red_team": specific_game.red_team.all(),
#         "blue_team": specific_game.blue_team.all(),
#         "winners": specific_game.winners,
#         "board": specific_game.board,
#     }

#     return render(request, 'games/detailed_game.html', context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
