import braintree
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from shop.recommender import Recommender
from .services import _get_list_of_products_from_the_order

from loguru import logger

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


@logger.catch
def payment_process(request):
    anon_user, created = User.objects.get_or_create(
                                                username='anonymous_user_00')
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # retrive nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # set order payer for different types of users
            if request.user.is_authenticated:
                order.payer = request.user
            else:
                order.payer = anon_user
            # get list of products that were bought together
            products = _get_list_of_products_from_the_order(order)
            if len(products) > 1:

                # store and score the products that were bought together.
                r = Recommender()
                r.products_bought(products)
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                      'client_token': client_token})

@logger.catch
def payment_done(request):
    return render(request, 'payment/done.html')

@logger.catch
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
