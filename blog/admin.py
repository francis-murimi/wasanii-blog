from django.contrib import admin
from .models import Category, Blog,Topic

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin) 

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'writer','blog_views', 'category','status', 'created', 'updated']
    list_filter = ['status','created', 'updated']
    list_editable = ['status','blog_views']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Blog, BlogAdmin) 

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name','created_on','active','likes']
    list_filter = ['created_on','active']
    list_editable = ['active','likes']
admin.site.register(Topic, TopicAdmin)
