
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..factories import OrderFactory


class OrderCreateTests(TestCase):

    def test_order_create_get(self):
        cart = {'1': {'quantity': 10, 'price': '25.00'}}
        currient_session = self.client.session
        currient_session['cart'] = cart
        currient_session.save()
        response = self.client.get('/en/orders/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order/create.html')
        self.assertContains(response, 'Checkout')
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')

    def test_order_create_post(self):
        response = self.client.post('/en/orders/create/',
                                    {'first_name': 'John',
                                     'last_name': 'Smith',
                                     'email': 'johnsmith@gmail.com',
                                     'address': 'Sonora st.',
                                     'postal_code': 52342, 'city': 'Miami'}
                                    )
        reverse_url = reverse('payment:process')
        self.assertRedirects(response, reverse_url, status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)


class AdminOrderDetailTests(TestCase):

    def setUp(self):
        User = get_user_model()
        new_user = User.objects.create_user('test_user123',
                                            'test4523@gmail.com',
                                            'testpass42142')
        self.get_user = User.objects.get(username='test_user123')
        self.get_user.is_staff = True
        self.get_user.save()

        self.order = OrderFactory()

    def test_admin_order_detail(self):
        self.client.login(username='test_user123', password='testpass42142')
        response = self.client.get('/en/orders/admin/order/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/orders/order/detail.html')
        self.assertContains(response, 'Order')
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')


class AdminOrderPDFTests(TestCase):

    def setUp(self):
        User = get_user_model()
        new_user = User.objects.create_user('test_user123',
                                            'test4523@gmail.com',
                                            'testpass42142')
        self.get_user = User.objects.get(username='test_user123')
        self.get_user.is_staff = True
        self.get_user.save()

        self.order = OrderFactory()

    def test_admin_order_PDF(self):
        self.client.login(username='test_user123', password='testpass42142')
        response = self.client.get('/en/orders/admin/order/1/pdf/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/pdf')
        self.assertTemplateUsed(response, 'orders/order/pdf.html')


class OrderListTests(TestCase):

    def setUp(self):
        User = get_user_model()
        new_user = User.objects.create_user('test_user123',
                                            'test4523@gmail.com',
                                            'testpass42142')
        get_user = User.objects.get(username='test_user123')

        self.order = OrderFactory(
            payer=get_user)

    def test_not_logged_in_user_redirected_to_login_page(self):
        response = self.client.get('/en/orders/order_list/')
        redirect_link = '/en/accounts/login/?next=%2Fen%2Forders%2Forder_list%2F'
        self.assertRedirects(response,
                             redirect_link,
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_order_list(self):
        self.client.login(username='test_user123', password='testpass42142')
        response = self.client.get('/en/orders/order_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/orders/order/order_list.html')
        self.assertContains(response, 'Orders')
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')


class OrderDetailTests(TestCase):

    def setUp(self):
        User = get_user_model()
        new_user = User.objects.create_user('test_user123',
                                            'test4523@gmail.com',
                                            'testpass42142')
        get_user = User.objects.get(username='test_user123')

        self.order = OrderFactory(
            payer=get_user)

    def test_not_logged_in_user_redirected_to_login_page(self):
        response = self.client.get('/en/orders/order_detail/1/')
        redirect_link = '/en/accounts/login/?next=%2Fen%2Forders%2Forder_detail%2F1%2F'
        self.assertRedirects(response, redirect_link, status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_order_detail(self):
        self.client.login(username='test_user123', password='testpass42142')
        response = self.client.get('/en/orders/order_detail/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/orders/order/order_detail.html')
        self.assertContains(response, 'Order')
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')
