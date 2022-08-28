from django.urls import path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views


app_name = "players"
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:name>/', views.PlayerView.as_view(), name='player'),
]

urlpatterns += staticfiles_urlpatterns()