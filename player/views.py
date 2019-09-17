from __future__ import absolute_import
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import InvitationForm, LoginForm, RegistrationForm
from .models import Invitation
from gameplay.models import Game


@login_required()
def home(request):
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.active()
    finished_games = my_games.difference(active_games)
    invitations = request.user.invitations_received.all()
    return render(request, "player/home.html",
                  {'active_games': active_games,
                   'finished_games': finished_games,
                   'invitations': invitations})


@login_required()
def new_invitation(request):
    if request.method == "POST":
        invitation = Invitation(from_user=request.user)
        form = InvitationForm(instance=invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = InvitationForm()
    return render(request, "player/new_invitation_form.html", {'form': form})


@login_required()
def accept_invitation(request, id):
    invitation = get_object_or_404(Invitation, pk=id)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        if "accept" in request.POST:
            game = Game.objects.create(
                first_player=invitation.to_user,
                second_player=invitation.from_user,
            )
        invitation.delete()
        return redirect(game)
    else:
        return render(request,
                      "player/accept_invitation_form.html",
                      {'invitation': invitation}
                      )

class LoginView(CreateView):
    form_class = LoginForm
    success_url = reverse_lazy('player_home')
    template_name = 'player/login_form.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class SignUpView(CreateView):
    form_class = RegistrationForm
    model = User
    template_name = "player/signup_form.html"
    success_url = reverse_lazy('player_home')

