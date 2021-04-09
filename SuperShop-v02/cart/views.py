import redis

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from loguru import logger

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender

@logger.catch
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@logger.catch
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
    #if cart:
    #    return redirect('cart:cart_detail')
    #return redirect('shop:product_list')

@logger.catch
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    coupon_apply_form = CouponApplyForm()

    try:
        r = Recommender()
        cart_products = [item['product'] for item in cart]
        recommended_products = r.suggest_products_for(cart_products,
                                                      max_results=4)
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Attention {e}")
        recommended_products = None

    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                  'coupon_apply_form': coupon_apply_form,
                  'recommended_products': recommended_products})
