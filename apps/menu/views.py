# apps/menu/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.menu.models import Category, Product
from apps.orders.models import CartItem


def menu_view(request):
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
    collection_mapping = {
        'hot_drinks': 'hot_drinks',
        'cold_drinks': 'cold_drinks',
        'Seasonal_Promotion': 'Seasonal_Promotion',
        'matcha': 'matcha',
        'healthy_menu': 'healthy_menu',
        'Brewed_coffee': 'Brewed_coffee',
        'tea': 'tea',
        'elcless': 'elcless',
        'cakes': 'cakes',
        'testbar': 'testbar',
        'crosan_sandwich': 'crosan_sandwich',
        'popsickle': 'popsickle'
    }

    collection_name = collection_mapping.get(category_name, category_name)
    products = Product.get_products_by_category(collection_name)

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
    print("=" * 50)
    print("👉 add_to_cart CALLED!")
    print(f"Method: {request.method}")
    print(f"User: {request.user}")
    print("=" * 50)

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        quantity = int(request.POST.get('quantity', 1))
        price_type = request.POST.get('price_type', '')
        image_url = request.POST.get('image_url', '')

        print(f"Product: {product_name}")
        print(f"Price: {price}")
        print(f"Quantity: {quantity}")
        print(f"Type: {price_type}")

        if not product_name:
            return JsonResponse({'status': 'error', 'message': 'Product name is required'})

        try:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product_name=product_name,
                price_type=price_type,
                defaults={
                    'product_price': price or 0,
                    'quantity': quantity,
                    'image_url': image_url or ''
                }
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            total_count = CartItem.objects.filter(user=request.user).aggregate(
                total=Sum('quantity')
            )['total'] or 0

            print(f"✅ Added! Total: {total_count}")
            print("=" * 50)

            return JsonResponse({
                'status': 'success',
                'cart_count': total_count
            })
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    print("❌ Not POST request")
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def get_cart_count(request):
    count = CartItem.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0
    return JsonResponse({'count': count})