from django.conf.urls import url
from django.urls import path
from . import views
from shop.views import art_add

app_name = 'shop'
urlpatterns = [
    path('add-art/',views.add_art,name='add_art'),
    path('art/add-art/',views.art_add.as_view(),name='art_add'),
    path('art/<int:artid>/preference/<int:userpreference>/',views.artpreference,name='artpreference'),
    path('art/art_list',views.art_list,name='art_list'),
    path('art/<category_slug>/',views.art_list,name='art_list_by_category'),
    path('art/<int:id>/<slug>/',views.art_detail,name='art_detail'),
    path('bidding/<int:id>/<slug>/',views.bidding,name='bidding'),
    path('art/bidding/<int:id>/<slug>/',views.bidding_detail,name='bidding_detail'),
    
]
