from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Post(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=1000,default="")
    published = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(max_length=255,default="")
    content = models.TextField(null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):  # Model bình luận
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Liên kết với Post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ai là người bình luận
    content = models.TextField()  # Nội dung bình luận
    created_at = models.DateTimeField(auto_now_add=True)  # Ngày giờ bình luận

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
