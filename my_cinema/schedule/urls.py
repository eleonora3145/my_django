from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.show_schedule, name='schedule'),
    path('main/', views.show_main, name='main'),
    path('movie/<int:movie_id>/', views.movie_info, name='movie_info'),
    path('seats/<int:screening_id>/', views.select_seats, name='select_seats'),
    path('get_seats/<int:screening_id>/', views.get_seats, name='get_seats'),
    path('buy_seats/', views.buy_seats, name='buy_seats'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('refund_ticket/<int:ticket_id>/', views.refund_ticket, name='refund_ticket'),
]