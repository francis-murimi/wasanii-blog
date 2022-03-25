from django.db import models 
from django.urls import reverse
from django.utils.text import slugify
from home.models import WriterProfile
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50,db_index=True)
    slug = models.SlugField(max_length=150,db_index=True,unique=True)
    description = models.TextField()
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('blog:blog_list_by_category',args=[self.slug])
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Blog(models.Model):
    STATUS = (
        (0,"Draft"),
        (1,"Publish")
        )
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    writer = models.ForeignKey(WriterProfile,related_name='owner',on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, db_index=True,unique=True)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    blog_views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)
    def get_blog_url(self):
        return reverse('blog:blog_detail',args=[self.id, self.slug])
    def archive_blog_url(self):
        return reverse('blog:archive_blog',args=[self.id])
    def publish_blog_url(self):
        return reverse('blog:publish_blog',args=[self.id])
    def edit_blog_url(self):
        return reverse('blog:edit_blog',args=[self.id])

class Preference(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='mtu')
    blog= models.ForeignKey(Blog,on_delete=models.CASCADE)
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.user) + ':' + str(self.blog) +':' + str(self.value)
    class Meta:
        unique_together = ("user", "blog", "value")

class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='commentor')
    body = models.CharField(max_length= 250)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['created_on']
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Topic(models.Model):
    name = models.CharField(max_length=49, help_text="Name of the topic")
    proposer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='proposer')
    description = models.TextField()
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_on']
    def get_topic_url(self):
        return reverse('blog:topic_detail',args=[self.id])

class TComment(models.Model):
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='topics')
    name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='commentator')
    body = models.CharField(max_length= 250)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['created_on']
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class TopicVote(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='voter')
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.user) + ':' + str(self.topic) +':' + str(self.value)
    class Meta:
        unique_together = ("user", "topic", "value")