from django.urls import path
from comment import views
from django.views.generic import ListView, DetailView
from comment.models import Post
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('article-detail/<str:post_url>/', views.article_detail, name='article_detail'),
    path('article-content/', views.article_content, name='article_content'),
]
