from django.urls import path
from comment import views
from django.views.generic import ListView, DetailView
from comment.models import Article
from django.contrib.auth import views as auth_views
from django.urls import re_path


urlpatterns = [
    re_path(r'^post-detail/(?P<post_url>\d+)/$', views.post_detail, name='post_detail'),
]
