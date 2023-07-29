# Generated by Django 4.0.2 on 2022-04-03 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wordofmouth', '0006_remove_recipe_likenum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=100)),
                ('commentText', models.CharField(max_length=200)),
                ('postTime', models.TimeField(auto_now_add=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wordofmouth.recipe')),
            ],
        ),
    ]
