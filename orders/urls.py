from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('my-bids/',views.my_orders,name='my_orders'),
    path('order/<order_id>/',views.order_detail, name='order_detail'),
    path('order_update/<order_id>/',views.order_update,name='order_update'),
]