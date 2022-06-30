from django.urls import path
from .views import *

urlpatterns = [
    path("", Home, name="home"),
    path('dashboard', index_view, name='dashboard_url'),
    path('turnir/', turnir_view, name='turnir_url'),
    path('tur/<int:pk>/', turnir_tur_view, name='tur_url'),
    path('matches/<int:pk>/', turnir_matches_view, name='matches_url'),
    path('add-tournament/', AddTournament, name='add-tournament'),
    path('add-round/', AddRound, name='add-round'),
    path('add-match/', AddMatch, name='add-match'),
    path('login', Loginpage, name="login"),
    path('logout/', LogoutView, name="logout"),
    path('close-match/', CloseMatch, name="close-match"),

]