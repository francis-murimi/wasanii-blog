from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    county = models.CharField(max_length=10)
    town = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10)
    description = models.TextField(help_text='A brief biography of yourself.')
    def __str__(self):
        return self.user.username
    def get_artist_detail(self):
        return reverse('home:artist_detail',args=[self.id])


class WriterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    town = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10)
    description = models.TextField( help_text='A brief biography of yourself.')
    def __str__(self):
        return self.user.username 
    def get_writer_detail(self):
        return reverse('home:writer_detail',args=[self.id])
