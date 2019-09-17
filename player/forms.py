from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from .models import Invitation


class InvitationForm(ModelForm):
    @property
    def helper(self):
        helper = FormHelper()
        helper.html5_required = False
        helper.form_tag = False
        return helper
    class Meta:
        model = Invitation
        exclude = ('from_user', 'timestamp')

class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password1',
            'password2',
            ButtonHolder(
                Submit('register', 'Register', css_class='btn btn-success')
            )
        )

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn btn-success')
            )
        )
