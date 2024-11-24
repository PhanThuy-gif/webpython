from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)  # Tiêu đề bài viết
    description = models.TextField()  # Nội dung tóm tắt
    content = models.TextField()  # Nội dung bài viết

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/article/{self.id}/"