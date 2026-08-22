# apps/orders/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import CartItem, Order, OrderItem
from apps.menu.models import Product
from django.db.models import Sum
import json


@login_required
def cart_view(request):
    """نمایش سبد خرید"""
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total() for item in cart_items)
    total_items = cart_items.count()

    context = {
        'cart_items': cart_items,
        'total': total,
        'total_items': total_items,
    }
    return render(request, 'orders/cart.html', context)


@login_required
def add_to_cart(request):
    """افزودن محصول به سبد خرید"""
    if request.method == 'POST':
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

            # دریافت تعداد کل آیتم‌های سبد خرید
            total_count = CartItem.objects.filter(user=request.user).aggregate(
                total=Sum('quantity')
            )['total'] or 0

            return JsonResponse({
                'status': 'success',
                'message': 'Added to cart',
                'cart_count': total_count
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def update_cart_item(request):
    """به‌روزرسانی تعداد یک آیتم در سبد خرید"""
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')  # 'increase' or 'decrease'

        try:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)

            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                else:
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Item removed',
                        'item_total': 0,
                        'cart_total': calculate_cart_total(request.user)
                    })
            cart_item.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Cart updated',
                'item_total': cart_item.get_total(),
                'cart_total': calculate_cart_total(request.user),
                'quantity': cart_item.quantity
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def remove_from_cart(request):
    """حذف یک آیتم از سبد خرید"""
    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        try:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            cart_item.delete()

            return JsonResponse({
                'status': 'success',
                'message': 'Item removed',
                'cart_total': calculate_cart_total(request.user)
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def clear_cart(request):
    """خالی کردن سبد خرید"""
    if request.method == 'POST':
        CartItem.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success', 'message': 'Cart cleared'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def calculate_cart_total(user):
    """محاسبه مجموع قیمت سبد خرید"""
    total = CartItem.objects.filter(user=user).aggregate(
        total=Sum('product_price', field='product_price * quantity')
    )['total'] or 0
    return float(total)


@login_required
def checkout(request):
    """تکمیل سفارش"""
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('menu:menu_list')

    if request.method == 'POST':
        total = sum(item.get_total() for item in cart_items)

        # ایجاد سفارش
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status='PENDING'
        )

        # ایجاد آیتم‌های سفارش
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item.product_name,
                product_price=item.product_price,
                quantity=item.quantity,
                price_type=item.price_type
            )

        # پاک کردن سبد خرید
        cart_items.delete()

        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('orders:order_success', order_id=order.id)

    total = sum(item.get_total() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success(request, order_id):
    """صفحه موفقیت سفارش"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        return render(request, 'orders/order_success.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, 'Order not found!')
        return redirect('core:home')


@login_required
def my_orders(request):
    """نمایش سفارشات کاربر"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_history(request):
    """نمایش تاریخچه سفارشات کاربر"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})


@login_required
def get_cart_count(request):
    """دریافت تعداد آیتم‌های سبد خرید (برای AJAX)"""
    count = CartItem.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0
    return JsonResponse({'count': count})