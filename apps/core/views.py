# apps/core/views.py (نسخه کامل با منو)

from django.shortcuts import render
from django.http import HttpResponse
from apps.menu.models import Category, Product


def home(request):
    """صفحه اصلی - نمایش ویدیو و دکمه منو"""
    return render(request, 'home.html')


def about(request):
    """صفحه درباره ما - نمایش اطلاعات کافه"""
    return render(request, 'about.html')


def contact(request):
    """صفحه تماس با ما - نمایش اطلاعات تماس"""
    return render(request, 'contact.html')


def menu_view(request):
    """صفحه منو - نمایش تمام دسته‌بندی‌ها"""
    # دریافت دسته‌بندی‌ها از MongoDB
    categories = Category.get_all_categories()

    # اگر دسته‌بندی در MongoDB وجود نداشت، از لیست پیش‌فرض استفاده کن
    if not categories:
        categories = [
            {'name': 'hot_drinks', 'persian_name': 'Hot Drinks', 'icon': 'fas fa-coffee'},
            {'name': 'cold_drinks', 'persian_name': 'Cold Drinks', 'icon': 'fas fa-glass-martini-alt'},
            {'name': 'Seasonal_Promotion', 'persian_name': 'Seasonal Promotion', 'icon': 'fas fa-star'},
            {'name': 'matcha', 'persian_name': 'Matcha', 'icon': 'fas fa-leaf'},
            {'name': 'healthy_menu', 'persian_name': 'Healthy Menu', 'icon': 'fas fa-heart'},
            {'name': 'Brewed_coffee', 'persian_name': 'Brewed Coffee', 'icon': 'fas fa-mug-hot'},
            {'name': 'tea', 'persian_name': 'Tea', 'icon': 'fas fa-tea'},
            {'name': 'elcless', 'persian_name': 'Silent Menu', 'icon': 'fas fa-moon'},
            {'name': 'cakes', 'persian_name': 'Cakes', 'icon': 'fas fa-birthday-cake'},
            {'name': 'testbar', 'persian_name': 'Toast Bar', 'icon': 'fas fa-bread'},
            {'name': 'crosan_sandwich', 'persian_name': 'Croissant Sandwich', 'icon': 'fas fa-sandwich'},
            {'name': 'popsickle', 'persian_name': 'Popsicle', 'icon': 'fas fa-ice-cream'}
        ]

    return render(request, 'menu/menu_list.html', {'categories': categories})


def menu_detail(request, category_name):
    """نمایش محصولات یک دسته‌بندی"""
    products = Product.get_products_by_category(category_name)

    # پیدا کردن نام دسته‌بندی
    category_names = {
        'hot_drinks': 'Hot Drinks',
        'cold_drinks': 'Cold Drinks',
        'Seasonal_Promotion': 'Seasonal Promotion',
        'matcha': 'Matcha',
        'healthy_menu': 'Healthy Menu',
        'Brewed_coffee': 'Brewed Coffee',
        'tea': 'Tea',
        'elcless': 'Silent Menu',
        'cakes': 'Cakes',
        'testbar': 'Toast Bar',
        'crosan_sandwich': 'Croissant Sandwich',
        'popsickle': 'Popsicle'
    }

    category = {
        'name': category_name,
        'persian_name': category_names.get(category_name, category_name),
        'description': f'Delicious {category_names.get(category_name, category_name)}'
    }

    return render(request, 'menu/menu_detail.html', {
        'category': category,
        'products': products
    })