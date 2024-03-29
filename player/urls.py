from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .views import home, new_invitation, accept_invitation, SignUpView, LoginView

urlpatterns = [
    url(r'home$', home, name="player_home"),
    url(r'login$',
        LoginView.as_view(),
        name="player_login"),
    url(r'logout$',
        LogoutView.as_view(),
        name="player_logout"),
    url(r'new_invitation$', new_invitation, name="player_new_invitation"),
    url(r'accept_invitation/(?P<id>\d+)/$',
        accept_invitation,
        name="player_accept_invitation"),
    url(r'signup$', SignUpView.as_view(), name='player_signup'),
]