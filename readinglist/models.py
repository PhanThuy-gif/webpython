from django.contrib.auth.models import User
from django.db import models
from home.models import Article  # Giả sử Article là model của bài báo

class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reading_list")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="saved_by")
    saved_at = models.DateTimeField(auto_now_add=True)  # Thời điểm lưu bài báo

    class Meta:
        unique_together = ('user', 'article')  # Một người dùng chỉ lưu một bài báo một lần
        ordering = ['-saved_at']  # Sắp xếp bài báo theo thời gian lưu
