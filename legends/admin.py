from django.contrib import admin
from .models import Legend, Comment

class LegendAdmin(admin.ModelAdmin):
    list_display = ['title','created_on','published']
    list_filter = ['created_on', 'published']
    list_editable = ['published']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Legend, LegendAdmin) 
