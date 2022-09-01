from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = "games"
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:game_datetime>/', views.GameView.as_view(), name='game'),
    path('submit_game', views.GameWizard.as_view(), name='submit'),
]

urlpatterns += staticfiles_urlpatterns()