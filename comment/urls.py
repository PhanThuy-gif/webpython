from django.urls import path
from . import views
from django.views.generic import ListView, DetailView
from .models import Post
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', ListView.as_view(
        queryset = Post.objects.all().order_by("-date"),
        template_name = 'comment/comment.html',
        context_object_name = 'Posts',
        paginate_by = 10)
        , name='comment'),
    path('<int:pk>/', views.post , name='post'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
