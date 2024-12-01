from django.urls import path
from django.contrib.auth import views as auth_views
from .views import post_detail, delete_comment



urlpatterns = [
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
]
