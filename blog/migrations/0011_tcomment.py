# Generated by Django 3.1.1 on 2021-05-20 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0010_auto_20210520_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='TComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=250)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentator', to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='blog.topic')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
