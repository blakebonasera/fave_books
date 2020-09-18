from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('book', views.success),
    path('logout', views.logout),
    path('login', views.login),
    path('addbook', views.newBook),
    path('book/<int:num>', views.book),
    path('book/<int:num>/update', views.update),
    path('book/<int:num>/delete', views.delete),
    path('book/<int:num>/favorite', views.favorite),
    path('book/<int:num>/unfavorite', views.unfavorite),
]