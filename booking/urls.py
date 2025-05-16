from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Bosh sahifa
    path('agent/<int:agent_id>/', views.booking_view, name='booking'),  # Agent uchun
    path('routes/', views.routes_view, name='routes'),  # Yo‘nalishlar
    path('tour_list/', views.tour_list_view, name='tour_list'),  # Reyslar ro'yxati
    path('set-language/', views.set_language, name='set_language'),  # Tilni almashtirish
    path('contact/', views.contact_view, name='contact'),  # Aloqa sahifasi
    path('login/', views.login_view, name='login'),  # Login sahifasi
]
