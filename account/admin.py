from django.contrib import admin
from .models import Profile
from home.models import Article
# Register your models here.

admin.site.register(Profile)
admin.site.register(Article)
