# Generated by Django 4.0.2 on 2022-05-02 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordofmouth', '0019_alter_ingredient_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentText',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='quantity',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='intro',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='step',
            name='text',
            field=models.CharField(max_length=300),
        ),
    ]