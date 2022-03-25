from django.contrib import admin
from . models import ArtistProfile,WriterProfile

class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ['user','county','town']
    list_filter = ['county','town']
    search_fields = ['user']
admin.site.register(ArtistProfile,ArtistProfileAdmin)

class WriterProfileAdmin(admin.ModelAdmin):
    list_display = ['user','age','town']
    list_filter = ['age','town']
    search_fields = ['user']
admin.site.register(WriterProfile,WriterProfileAdmin)