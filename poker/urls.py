from django.urls import path
from .views import index, detail, createGame, createRound, apiEndGame, apiGetRound, apiDeleteRound

urlpatterns = [
    path('', index, name="poker_index"),
    path('<int:id>/', detail, name="poker_detail"),
    path('create_game/', createGame, name="poker_create_game"),
    path('create_round/<int:game_id>/', createRound, name="poker_create_round"),
    path('api/end_game/<int:game_id>/', apiEndGame, name="poker_end_game"),
    path('api/getRound/<int:round_id>/', apiGetRound, name="poker_get_round"),
    path('api/deleteRound/<int:round_id>/', apiDeleteRound, name="poker_delete_round"),
]