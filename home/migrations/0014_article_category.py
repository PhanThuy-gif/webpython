# Generated by Django 5.1.2 on 2024-11-18 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_article_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
