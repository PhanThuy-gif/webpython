from django.db import models
from django.utils.timezone import now
from home.models import Article
from django.conf import settings


class Comment(models.Model):  # Model bình luận
    post = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ai là người bình luận
    content = models.TextField()  # Nội dung bình luận
    created_at = models.DateTimeField(auto_now_add=True)  # Ngày giờ bình luận

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
