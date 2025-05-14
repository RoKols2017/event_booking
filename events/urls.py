# events/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/book/', views.book_event, name='book_event'),
    path('confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('register/', views.register_user, name='register'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]

