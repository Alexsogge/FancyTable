from django.urls import path
from . import views
from .socket_connection import load_saved_config_file


urlpatterns = [
    path('', views.index, name='index'),
    path('control/', views.control, name='control'),
    path('config/', views.configs, name='configs'),
    path('config/<int:extension_id>/', views.config, name='config'),
    path('extension_select/', views.extension_select, name='extension_select'),
    path('highscore_page/', views.highscore_page, name='highscore_page'),
    path('highscores/<int:extension_id>/', views.highscores, name='highscores'),
]


load_saved_config_file()