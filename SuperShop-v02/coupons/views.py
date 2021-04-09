from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from loguru import logger

from .models import Coupon
from .forms import CouponApplyForm

from cart.cart import Cart
from orders.services import _check_cart_length_greater_than_zero

@logger.catch
@require_POST
def coupon_apply(request):
    cart = request.session['cart']
    _check_cart_length_greater_than_zero(cart)
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
