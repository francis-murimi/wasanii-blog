# Generated by Django 3.1.1 on 2021-05-14 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_art_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='art',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
    ]