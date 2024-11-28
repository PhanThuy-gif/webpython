from django.db import models
from django.conf  import settings


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments") # xóa bài viết xóa luôn bình luận,tìm các bình luận thông qua từ khóa comments
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
