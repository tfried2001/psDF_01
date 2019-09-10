from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .models import Invitation
from .forms import InvitationForm
from gameplay.models import Game

# Create your views here.

# @login_required states that this view is only availabe to authenticated users
@login_required
def home(request):
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.active()
    my_invitations = Invitation.objects.my_invitations(request.user)
    sent_invitations = Invitation.objects.sent_invitations(request.user)

    return render(request, 'player/home.html',
                  {'activeGames': active_games,
                  'myGames': my_games,
                  'myInvitations': my_invitations,
                  'sentInvitations': sent_invitations})


@login_required
def new_invitation(request):
    if request.method == "POST":
        invitation = Invitation(from_user=request.user)
        form = InvitationForm(instance=invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = InvitationForm()
    return render(request, 'player/new_invitation_form.html', {'form': form})
