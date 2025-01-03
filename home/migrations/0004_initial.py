# Generated by Django 5.1.2 on 2024-11-14 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0003_delete_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('link', models.URLField(unique=True)),
                ('content', models.TextField(default='')),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
