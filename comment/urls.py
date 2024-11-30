from django.urls import path
from comment import views
from django.views.generic import ListView, DetailView
from comment.models import Post
from django.contrib.auth import views as auth_views
from django.urls import re_path


urlpatterns = [
    re_path(r'^article-detail/(?P<post_url>\d+)/$', views.article_detail, name='article_detail'),
    path('article-content/', views.article_content, name='article_content'),
]
