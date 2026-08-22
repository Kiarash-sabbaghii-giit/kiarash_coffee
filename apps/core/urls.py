# apps/core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('art/', views.art, name='art'),          # <-- اضافه کنید
    path('contact/', views.contact, name='contact'),
]