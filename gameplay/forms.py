from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from .models import Move

class MoveForm(ModelForm):
    helper = FormHelper()
    class Meta:
        model = Move
        exclude = []