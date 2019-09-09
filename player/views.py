from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .forms import InvitationForm
from gameplay.models import Game

# Create your views here.

# @login_required states that this view is only availabe to authenticated users
@login_required
def home(request):
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.active()

    return render(request, 'player/home.html',
                  {'activeGames': active_games, 'myGames': my_games})


@login_required
def new_invitation(request):
    form = InvitationForm()
    return render(request, 'player/new_invitation_form.html', {'form': form})
    