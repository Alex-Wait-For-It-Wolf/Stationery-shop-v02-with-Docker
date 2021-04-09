from django.test import TestCase
from django.urls import reverse, resolve

from shop.factories import CategoryFactory, ProductFactory
from ..views import cart_detail, cart_add, cart_remove


class TestCartDetailView(TestCase):

    def test_cart_detail_url_resolves_detail_view(self):
        view = resolve('/en/cart/')
        self.assertEqual(view.func.__name__, cart_detail.__name__)

    def test_get_cart_detail_view(self):
        response = self.client.get('/en/cart/')
        self.assertEqual(response.status_code, 200)

class TestCartAddView(TestCase):

    def test_cart_add_redirect_to_cart(self):
        product = ProductFactory(
            id=1,
            name='Mitsubishi',
            slug='mitsubishi',
            description='some car',
            category__name='cars',
            price=12005,
        )
        response = self.client.post('/en/cart/add/1/', {'id': 1})
        self.assertRedirects(response, '/en/cart/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_cart_add_url_resolves_add_view(self):
        view = resolve('/en/cart/add/1/')
        self.assertEqual(view.func.__name__, cart_add.__name__)


class TestCartRemoveView(TestCase):

    def test_cart_remove_redirect_to_cart(self):
        product = ProductFactory(
            id=1,
            name='Mitsubishi',
            slug='mitsubishi',
            description='some car',
            category__name='cars',
            price=12005,
        )
        response = self.client.post('/en/cart/remove/1/', {'id': 1})
        self.assertRedirects(response, '/en/cart/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_cart_remove_url_resolves_add_view(self):
        view = resolve('/en/cart/remove/1/')
        self.assertEqual(view.func.__name__, cart_remove.__name__)
