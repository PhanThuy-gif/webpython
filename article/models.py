from django.db import models
from django.contrib.auth.models import User
from home.models import Article

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments", verbose_name="Article")
    content = models.TextField(verbose_name="Comment Content")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title} at {self.created_at}"
