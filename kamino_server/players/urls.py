from django.urls import path

from . import views


app_name = "players"
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:player_name>/', views.player, name='player'),
]