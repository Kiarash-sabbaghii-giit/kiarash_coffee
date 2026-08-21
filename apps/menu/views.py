# apps/menu/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from apps.menu.models import Category, Product
from django.contrib.auth.decorators import login_required
from django.db import models


def menu_view(request):
    """صفحه منو"""
    categories = Category.get_all_categories()

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


@login_required
def add_to_cart(request):
    """افزودن محصول به سبد خرید"""
    if request.method == 'POST':
        from apps.orders.models import CartItem

        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        quantity = int(request.POST.get('quantity', 1))
        price_type = request.POST.get('price_type', '')
        image_url = request.POST.get('image_url', '')

        try:
            # بررسی وجود محصول در سبد خرید
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product_name=product_name,
                price_type=price_type,
                defaults={
                    'product_price': price,
                    'quantity': quantity,
                    'image_url': image_url
                }
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({'status': 'success', 'message': 'Added to cart'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def get_cart_count(request):
    """دریافت تعداد آیتم‌های سبد خرید"""
    from apps.orders.models import CartItem
    from django.db.models import Sum

    count = CartItem.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return JsonResponse({'count': count})