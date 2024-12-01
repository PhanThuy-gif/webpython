from django.urls import path
from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^post-detail/(?P<post_url>\d+)/$', views.post_detail, name='post_detail'),

]
