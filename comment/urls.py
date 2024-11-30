from django.urls import path
from . import views
from django.views.generic import ListView, DetailView
from .models import Post
from django.contrib.auth import views as auth_views
from django.urls import re_path

urlpatterns = [
    re_path(r'^article-detail/(?P<article_url>.+)/$', views.article_detail, name='article_detail'),  # Sử dụng re_path để xử lý URL mã hóa
    
]
