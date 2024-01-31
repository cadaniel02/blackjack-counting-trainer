# game/urls.py

from django.urls import path
from .views import JoinGame, CreateOrGetPlayerView, GetCurrentGame

urlpatterns = [
    path('join/<int:game_id>/', JoinGame.as_view(), name='join_game'),
    path('get_player/', CreateOrGetPlayerView.as_view(), name='create_player'),
    path('get_game/', GetCurrentGame.as_view(), name='get_current_game')
]
