from django.db import models
from shop.models import Art
from django.contrib.auth.models import User
from django.urls import reverse

class Order(models.Model):
    orderer = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Art,related_name='order_item',on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    first_name = models.CharField(max_length=60) 
    last_name = models.CharField(max_length=60)
    phone_number = models.CharField(max_length= 10)
    delivery_point = models.CharField(max_length=70,help_text='Building or hostel')
    area = models.CharField(max_length=70, help_text='e.g V.M,Muranga Town')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    packaged = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('orders:order_detail',args=[self.id])
    
    def get_order_update(self):
        return reverse('orders:order_update',args=[self.id])

class Bids(models.Model):
    bidder = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Art,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)   