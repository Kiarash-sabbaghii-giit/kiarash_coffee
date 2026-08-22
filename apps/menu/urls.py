# apps/menu/urls.py

from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_view, name='menu_list'),
    path('<str:category_name>/', views.menu_detail, name='menu_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),      # <-- این خط
    path('cart-count/', views.get_cart_count, name='cart_count'),
]