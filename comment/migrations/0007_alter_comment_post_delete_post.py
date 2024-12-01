# Generated by Django 5.1.2 on 2024-11-30 23:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_remove_post_created_at_remove_post_url_post_category_and_more'),
        ('home', '0014_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='home.article'),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
