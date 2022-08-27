from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views


app_name = "games"
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:game_datetime>/', views.GameView.as_view(), name='game'),
]

urlpatterns += staticfiles_urlpatterns()