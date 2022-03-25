from django.contrib import admin
from .models import Order, Bids

class OrderAdmin(admin.ModelAdmin):
    list_display = ['orderer', 'product','cost','paid','packaged', 'delivered']
    list_filter = ['paid','created', 'delivered']
    list_editable = ['paid', 'delivered', 'packaged']
admin.site.register(Order, OrderAdmin)

class BidsAdmin(admin.ModelAdmin):
    list_display = ['bidder', 'product','amount', 'created']
    list_filter = ['amount','created','product']
admin.site.register(Bids, BidsAdmin)


