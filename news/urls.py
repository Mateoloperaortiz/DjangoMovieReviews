# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name='news_home'),
] 