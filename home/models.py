from django.db import models
from django.utils.timezone import now

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