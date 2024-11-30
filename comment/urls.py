from django.urls import path
from . import views
from django.views.generic import ListView, DetailView
from .models import Post
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
