import base64

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from ..factories import OrderFactory


class OrderListTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.new_user = User.objects.create_user('test_user123',
                                                 'test4523@gmail.com',
                                                 'testpass42142')

        self.second_user = User.objects.create_user('test_user1234',
                                                 'test2222@gmail.com',
                                                 'testpass2222')

        self.order_01 = OrderFactory(
            first_name='Bob',
            payer=self.new_user,
        )
        self.order_02 = OrderFactory(
            first_name='Will',
            payer=self.new_user,
        )
        self.order_03 = OrderFactory(
            first_name='John',
            payer=self.new_user,
        )
        self.order_04 = OrderFactory(
            first_name='Clint',
            payer=self.second_user,
        )

    def test_no_access_without_authorization(self):
        url = reverse('api_orders:order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_no_access_with_wrong_credentials(self):
        user_name = 'wrong_user'
        user_pass = 'wrong_pass'
        credentials = base64.b64encode(
            f'{user_name}:{user_pass}'.encode('utf-8')
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Basic {}'.format(credentials.decode('utf-8'))
        )
        url = reverse('api_orders:order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_got_access_with_authentication(self):
        self.client.force_authenticate(user=self.new_user)
        url = reverse('api_orders:order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order_01.first_name)
        self.assertNotContains(response, 'something, that not in order')

    def test_got_access_only_to_personal_orders(self):
        self.client.force_authenticate(user=self.new_user)
        url = reverse('api_orders:order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order_01.first_name)
        self.assertContains(response, self.order_02.first_name)
        self.assertContains(response, self.order_03.first_name)
        self.assertNotContains(response, self.order_04.first_name)
