from django.http import Http404

from loguru import logger


@logger.catch
def _check_order_payer(payer, request):
    """Check if logged user match requested order."""
    if payer != request.user:
        raise Http404

@logger.catch
def _check_cart_length_greater_than_zero(cart):
    """Rise Error404 if lenght of cart items less than 1"""
    items_in_the_cart = [item for item in cart]
    if len(items_in_the_cart) < 1:
            raise Http404
