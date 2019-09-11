from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from .models import Invitation

class InvitationForm(ModelForm):
    helper = FormHelper()
    class Meta:
        model = Invitation
        exclude = ('from_user', 'timestamp')
