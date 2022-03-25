from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from home.models import ArtistProfile
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=20,db_index=True)
    slug = models.SlugField(max_length=150,db_index=True,unique=True)
    description = models.TextField()
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:art_list_by_category',args=[self.slug])
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Art(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    artist = models.ForeignKey(ArtistProfile,related_name='owner',on_delete=models.CASCADE)
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True,unique=True)
    image_1 = models.ImageField(upload_to='products/%Y/%m/%d')
    image_2 = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)
    available = models.BooleanField(default=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Art, self).save(*args, **kwargs)
    def get_art_url(self):
        return reverse('shop:art_detail',args=[self.id, self.slug])
    def go_bidding(self):
        return reverse('shop:bidding',args=[self.id, self.slug])

class Preference(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    art= models.ForeignKey(Art,on_delete=models.CASCADE)
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.user) + ':' + str(self.art) +':' + str(self.value)
    class Meta:
        unique_together = ("user", "art", "value")