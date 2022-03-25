from django.contrib import admin
from .models import Category, Art

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class ArtAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'category','bid_price','available', 'created', 'updated']
    list_filter = ['available','created', 'updated']
    list_editable = ['bid_price', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Art, ArtAdmin)


