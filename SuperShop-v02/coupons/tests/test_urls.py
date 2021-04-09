from django.test import Client, TestCase, RequestFactory
from django.urls import reverse

from ..models import Coupon
from ..views import coupon_apply
from shop.factories import ProductFactory


class CouponApplyTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.product = ProductFactory()
        self.cart = {'1': {'quantity': 3,
                           'price': '25.00'}}

    def test_coupon_apply_invalid_code_redirect_post(self):
        currient_session = self.client.session
        currient_session['cart'] = self.cart
        currient_session.save()
        response = self.client.post('/en/coupons/apply/', {'code': 'Winter',})
        reverse_url = reverse('cart:cart_detail')
        self.assertRedirects(response, reverse_url, status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_coupon_apply_valid_code_redirect_post(self):
        new_coupon = Coupon.objects.create(code='Summer',
                                        valid_from='2021-02-21 20:21:51+00:00',
                                        valid_to='2022-02-21 20:21:51+00:00',
                                        discount=50,
                                        active=True)
        request = self.factory.post('/en/coupons/apply/')
        new_session = self.client.session
        request.session = new_session
        request.session['cart'] = self.cart

        coupon_id = _get_coupon_id_or_return_none(request)
        self.assertEqual(coupon_id, None)

        form_data = {'code': 'Summer'}
        request.POST = form_data
        response = coupon_apply(request)
        response.client = Client()

        coupon_id = _get_coupon_id_or_return_none(request)
        self.assertEqual(coupon_id, new_coupon.id)

        reverse_url = reverse('cart:cart_detail')
        self.assertRedirects(response, reverse_url, status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

def _get_coupon_id_or_return_none(request):
    try:
        coupon_id = request.session['coupon_id']
    except KeyError:
        coupon_id = None
    return coupon_id
