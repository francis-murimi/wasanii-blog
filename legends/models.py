from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

class Legend(models.Model):
    title = models.CharField(max_length=200,db_index=True,unique=True)
    slug = models.SlugField(max_length=220, db_index=True,unique=True)
    story = models.TextField()
    published = models.BooleanField(default=False)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_on']
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Legend, self).save(*args, **kwargs)
    def get_legend_url(self):
        return reverse('legends:legend_detail',args=[self.id])


class Preference(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='guy')
    legend= models.ForeignKey(Legend,on_delete=models.CASCADE)
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.user) + ':' + str(self.legend) +':' + str(self.value)
    class Meta:
        unique_together = ("user", "legend", "value")


class Comment(models.Model):
    legend = models.ForeignKey(Legend,on_delete=models.CASCADE,related_name='opinion')
    name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='commenter')
    body = models.CharField(max_length= 250)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_on']
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)