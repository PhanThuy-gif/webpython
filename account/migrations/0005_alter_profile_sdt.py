# Generated by Django 5.1.2 on 2024-11-03 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_sdt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sdt',
            field=models.CharField(max_length=55, null=True, unique=True, verbose_name='sdt'),
        ),
    ]
