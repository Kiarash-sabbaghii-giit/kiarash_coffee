# apps/orders/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CartItem, Order, OrderItem


@login_required
def cart_view(request):
    """نمایش سبد خرید"""
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total() for item in cart_items)
    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def checkout(request):
    """تکمیل سفارش"""
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items:
            return redirect('menu:menu_list')

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

        return render(request, 'orders/order_success.html', {'order': order})

    return redirect('orders:cart')


@login_required
def my_orders(request):
    """نمایش سفارشات کاربر"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})