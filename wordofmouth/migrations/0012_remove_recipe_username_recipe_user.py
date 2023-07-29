# Generated by Django 4.0.2 on 2022-04-16 22:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wordofmouth', '0011_recipe_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='username',
        ),
        migrations.AddField(
            model_name='recipe',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]