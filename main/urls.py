from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('logout', views.logout),
    path('login', views.login),
    path('addbook', views.newBook),
    path('book/<int:num>', views.book),
]