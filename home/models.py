from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    published = models.DateTimeField(null=True, blank=True)
    summary = models.TextField()
    content = models.TextField(null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments", verbose_name="Article")
    content = models.TextField(verbose_name="Comment Content")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title} at {self.created_at}"
