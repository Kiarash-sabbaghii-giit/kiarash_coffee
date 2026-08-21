# apps/core/context_processors.py

from apps.orders.models import CartItem


def cart_count(request):
    """Context processor برای نمایش تعداد آیتم‌های سبد خرید در تمام صفحات"""
    if request.user.is_authenticated:
        try:
            from django.db.models import Sum
            count = CartItem.objects.filter(user=request.user).aggregate(
                total=Sum('quantity')
            )['total'] or 0
        except:
            count = 0
    else:
        count = 0

    return {
        'cart_count': count
    }