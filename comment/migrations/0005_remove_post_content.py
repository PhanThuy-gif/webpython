# Generated by Django 5.1.2 on 2024-11-30 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_post_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
    ]
