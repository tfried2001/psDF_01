from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.db.models import Q as orQuery
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

GAME_STATUS_CHOICES = (
    ('F', 'First Player To Move'),
    ('S', 'Second Player To Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw'),
)

BOARD_SIZE = 3

class GamesQuerySet(models.QuerySet):
    def games_for_user(self, user):
        return self.filter(
            orQuery(first_player=user) | orQuery(second_player=user)
        )

    def active(self):
        return self.filter(
            orQuery(status='F') | orQuery(status='S')
        )


@python_2_unicode_compatible
class Game(models.Model):
    first_player = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="games_first_player")
    second_player = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="games_second_player")

    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(
        default='F', max_length=1, choices=GAME_STATUS_CHOICES)

    objects = GamesQuerySet.as_manager()

    def board(self):
        """Return a 2-dimensional list of Move objects,
        so you can ask for the state of a square at position [y][x]."""
        board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        for move in self.move_set.all():
            board[move.y][move.x] = move
        return board

    def is_users_move(self, user):
        return (user == self.first_player and self.status == 'F') or\
            (user == self.second_player and self.status == 'S')

    def get_absolute_url(self):
        return reverse('gameplay_detail', args=[self.id])

    def __str__(self):
        return "{0} vs {1}".format(
            self.first_player, self.second_player
        )


class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=300, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, editable=False)
    by_first_player = models.BooleanField(editable=False)
