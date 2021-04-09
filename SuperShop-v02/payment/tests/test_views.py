from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from ..views import payment_process
from orders.factories import OrderFactory

class PaymentProcessTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.order = OrderFactory()

    def test_payment_process(self):
        request = self.factory.get('/en/payment/process/')
        request.session = self.client.session
        request.session['order_id'] = self.order.id
        response = payment_process(request)
        self.assertEqual(response.status_code, 200)
