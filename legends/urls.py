from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'legends'
urlpatterns = [
    path('<int:id>/',views.legend_detail,name='legend_detail'),
    path('legend/<int:legendid>/preference/<int:userpreference>/',views.legendpreference,name='legendpreference'),
    path('legend-list',views.legend_list,name='legend_list'),
    
]