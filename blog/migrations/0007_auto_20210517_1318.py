# Generated by Django 3.1.1 on 2021-05-17 13:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_auto_20210517_1313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preference',
            old_name='art',
            new_name='blog',
        ),
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together={('user', 'blog', 'value')},
        ),
    ]