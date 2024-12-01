from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    path('',views.index,name='home'),
    path('search/', views.search, name='search'),
    path('<str:category>/', views.category_view, name='category_view'),
    re_path(r'^article-detail/(?P<article_url>.+)/$', views.article_detail, name='article_detail'),  # Sử dụng re_path để xử lý URL mã hóa
]

