# Generated by Django 5.1.2 on 2024-11-14 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_article_content'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
    ]
