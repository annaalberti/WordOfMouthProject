# Generated by Django 4.0.2 on 2022-05-03 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordofmouth', '0020_alter_comment_commenttext_alter_ingredient_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentText',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='step',
            name='text',
            field=models.CharField(max_length=2000),
        ),
    ]
