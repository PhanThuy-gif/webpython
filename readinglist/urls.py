from django.urls import path
from .views import add_to_reading_list, remove_from_reading_list, reading_list_view
from . import views

urlpatterns = [
    path('reading-list/add/<int:article_id>/', views.add_to_reading_list, name='add_to_reading_list'),
    path('reading-list/remove/<int:article_id>/', views.remove_from_reading_list, name='remove_from_reading_list'),
    path('reading-list/', views.reading_list_view, name='reading_list'),
]
