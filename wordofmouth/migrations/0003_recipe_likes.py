# Generated by Django 4.0.2 on 2022-03-24 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordofmouth', '0002_alter_image_src'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='likes',
            field=models.BigIntegerField(default=0, max_length=8),
        ),
    ]
