from django.db import models

from django.db.models import Q as orQuery
from django.contrib.auth.models import User
# Create your models here.

class InvitationQuerySet(models.QuerySet):
    def received_invitations(self, user):
        return self.filter(
            orQuery( from_user = user )
        )

    def sent_invitations(self, user):
        return self.filter(
            orQuery( to_user = user )
        )


class Invitation(models.Model):
    from_user = models.ForeignKey(User, related_name="invitations_sent", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="invitations_received", on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = InvitationQuerySet.as_manager()

    def __str__(self):
        return "From: {0}, To: {1}, Message: {2}".format(
            self.from_user,
            self.to_user,
            self.message
        )
