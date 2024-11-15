from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    path('',views.index,name='home'),
    path('thoi-su/', views.index, name='thoi_su'),
    path('the-gioi/', views.index, name='the_gioi'),
    path('video/', views.index, name='video'),
    path('kinh-doanh/', views.index, name='kinh_doanh'),
    path('bat-dong-san/', views.index, name='bat_dong_san'),
    path('khoa-hoc/', views.index, name='khoa_hoc'),
    path('gia-tri/', views.index, name='giai_tri'),
    path('the-thao/', views.index, name='the_thao'),
    path('phap-luat/', views.index, name='phap_luat'),
    path('giao-duc/', views.index, name='giao_duc'),
    path('suc-khoe/', views.index, name='suc_khoe'),
    path('doi-song/', views.index, name='doi_song'),
    path('du-lich/', views.index, name='du_lich'),
    path('so-hoa/', views.index, name='so_hoa'),
    path('xe/', views.index, name='xe'),
    re_path(r'^article-detail/(?P<article_url>.+)/$', views.article_detail, name='article_detail'),  # Sử dụng re_path để xử lý URL mã hóa
]

