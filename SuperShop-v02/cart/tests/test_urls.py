from django.urls import reverse, resolve
from django.test import TestCase

from shop.factories import ProductFactory


class CartDetailTests(TestCase):

    def test_cart_detail(self):
        response = self.client.get('/en/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertContains(response, 'Your shopping cart')
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')

        product = ProductFactory(
            id=1,
            name='Mitsubishi',
            slug='mitsubishi',
            description='some car',
            category__name='cars',
            price=12005,
        )

        url = reverse('cart:cart_detail')
        self.assertEqual(url, '/en/cart/')
        resolver = resolve('/en/cart/')
        self.assertEqual(resolver.view_name, 'cart:cart_detail')
        self.assertEqual(resolver.url_name, 'cart_detail')
        self.assertEqual(resolver.app_name, 'cart')


class CartAddTests(TestCase):

    def test_cart_add(self):
        product = ProductFactory(
            id=1,
            name='Mitsubishi',
            slug='mitsubishi',
            description='some car',
            category__name='cars',
            price=12005,
        )

        response = self.client.post('/en/cart/add/1/', {'id': 1})
        #self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/en/cart/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

        url = reverse('cart:cart_add', kwargs={'product_id':1})
        self.assertEqual(url, '/en/cart/add/1/')
        resolver = resolve('/en/cart/add/1/')
        self.assertEqual(resolver.view_name, 'cart:cart_add')
        self.assertEqual(resolver.url_name, 'cart_add')
        self.assertEqual(resolver.app_name, 'cart')


class CartRemoveTests(TestCase):

    def test_cart_remove(self):

        product = ProductFactory(
            id=1,
            name='Mitsubishi',
            slug='mitsubishi',
            description='some car',
            category__name='cars',
            price=12005,
        )

        add_to_cart = self.client.post('/en/cart/add/1/')
        response = self.client.post('/en/cart/remove/1/')
        self.assertRedirects(response, '/en/cart/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

        url = reverse('cart:cart_remove', kwargs={'product_id':1})
        self.assertEqual(url, '/en/cart/remove/1/')
        resolver = resolve('/en/cart/remove/1/')
        self.assertEqual(resolver.view_name, 'cart:cart_remove')
        self.assertEqual(resolver.url_name, 'cart_remove')
        self.assertEqual(resolver.app_name, 'cart')
