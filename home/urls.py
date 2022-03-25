from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
app_name = 'home'
urlpatterns = [
    path('',views.home,name = 'home'),
    path('artist-register/',views.artist_register,name='artist_register'),
    path('writer-register/',views.writer_register,name='writer_register'),
    path('buyer-register/',views.buyer_register,name='buyer_register'),
    path('login/',views.log_in,name='log_in'),
    path('logout/',views.log_out,name='log_out'),
    path('artist/<int:id>/',views.artist_detail,name='artist_detail'),
    path('writer/<int:id>/',views.writer_detail,name='writer_detail'),
] 