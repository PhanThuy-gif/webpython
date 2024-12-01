from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from home.models import Article


class Comment(models.Model):  # Model bình luận
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ai là người bình luận
    content = models.TextField()  # Nội dung bình luận
    created_at = models.DateTimeField(auto_now_add=True)  # Ngày giờ bình luận

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
