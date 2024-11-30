from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):  # Đây là model bài viết cơ bản
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):  # Model bình luận
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',null=True, blank=True)  # Liên kết với Post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ai là người bình luận
    content = models.TextField()  # Nội dung bình luận
    created_at = models.DateTimeField(auto_now_add=True)  # Ngày giờ bình luận

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
