from django.contrib import auth
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import login
from django.contrib.auth.models import User

from orders.models import Order, OrderItem
from shop.models import Category, Product
from ..views import payment_process


class PaymentProcessTests(TestCase):
    """
    This error (ErrorResult 'Gateway Rejected: duplicate') occurres
    not because of wrong test of view, but because your Braitree
    account have the Duplication Transaction Checking option
    enabled. (You can check nonce or result in views)
    more info:
    https://stackoverflow.com/questions/40520623/when-creating
    -transaction-with-fake-valid-nonce-in-test-the-transaction-result
    You have two options:
    1. Log into your Braintree Control Panel and go to
    Settings > Processing > Edit or Disable under Duplicate Transaction
    Settings.
    2. Run test_payment_process_post_done_user_is_anonymous and
    test_payment_process_post_done_user_is_authenticated one-by-one but
    with small time-out.
    """

    def setUp(self):
        self.factory = RequestFactory()

        self.category = Category.objects.create(
        name='Coffee',
        slug='coffe',
        )
        self.product = Product.objects.create(
        name='Cappucino',
        slug='cappucino',
        description='some coffee',
        category=self.category,
        price=125,
        )
        self.order = Order.objects.create(
        first_name='John',
        last_name='Doe',
        email='johndoe@inabox.com',
        address='Sunset Blv 17',
        postal_code=45345,
        city='Miami',
        created='auto',
        updated='auto',
        paid=False,
        braintree_id='2sr455xjv2xf3css',
        coupon=None,
        discount=0,
        payer=None,
        )
        self.order_item = OrderItem.objects.create(
        order=self.order,
        product=self.product,
        price=25,
        quantity=3,
        )

        self.nonce = {'payment_method_nonce': 'fake-valid-nonce'}

    def test_payment_process_get(self):
        request = self.factory.get('/en/payment/process/')
        request.session = self.client.session
        request.session['order_id'] = self.order.id
        response = payment_process(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pay by credit card')
        self.assertNotContains(response,
                               'Hi there! I should not be on the page.')

    def test_payment_process_post_done_user_is_anonymous(self):
        important_message = """If error '/en/payment/done/ !=
        /en/payment/canceled/' have occurred,
        read PaymentProcessTests comment."""
        print(important_message)

        request = self.factory.post('/en/payment/process/')
        request.session = self.client.session
        request.session['order_id'] = self.order.id

        request.POST = self.nonce

        client = Client()
        user = auth.get_user(client)
        self.assertTrue(user.is_anonymous)
        request.user = user

        response = payment_process(request)
        response.client = Client()
        self.assertRedirects(response, '/en/payment/done/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_payment_process_post_done_user_is_authenticated(self):

        request = self.factory.post('/en/payment/process/')
        request.session = self.client.session
        request.session['order_id'] = self.order.id

        user = User.objects.create(username='testuser01',
                                   password='testpass02')
        login(request, user)
        self.assertTrue(user.is_authenticated)

        request.POST = self.nonce
        request.user = user

        response = payment_process(request)
        response.client = Client()
        self.assertRedirects(response, '/en/payment/canceled/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_post_canceled_without_nonce(self):

        request = self.factory.post('/en/payment/process/')
        request.session = self.client.session
        request.session['order_id'] = self.order.id

        client = Client()
        user = auth.get_user(client)
        request.user = user

        response = payment_process(request)
        response.client = Client()
        self.assertRedirects(response, '/en/payment/canceled/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)


class PaymentDoneTests(TestCase):

    def test_payment_done(self):
        response = self.client.get('/en/payment/done/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/done.html')
        self.assertContains(response, 'Your payment was successful')
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')


class PaymentCanceledTests(TestCase):

    def test_payment_canceled(self):
        response = self.client.get('/en/payment/canceled/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/canceled.html')
        self.assertContains(response, 'Your payment has not been processed')
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')
