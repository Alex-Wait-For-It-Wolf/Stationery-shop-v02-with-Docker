from django.test import RequestFactory, TestCase
from django.urls import reverse, resolve

from shop.factories import ProductFactory
from ..cart import Cart

class CartAddTests(TestCase):

    def setUp(self):

        # vars, that allow us run Cart.add() method for tests
        self.session = self.client.session
        self.cart = {}
        save = self.save

        self.empty_cart = {}
        self.default_quantity = 1
        self.random_quantity_01 = 5
        self.random_quantity_02 = 13
        self.product = ProductFactory(
            id=1,
            name='Mitsubishi',
            slug='mitsubishi',
            description='some car',
            category__name='cars',
            price=12005,
        )

    def test_add_product_to_the_cart_with_default_quantity(self):

        self.assertEqual(self.cart, self.empty_cart)
        add_method = Cart.add(self, self.product)
        self.assertEqual(int(self.cart['1']['price']), self.product.price)
        self.assertEqual(self.cart['1']['quantity'], self.default_quantity)

    def test_add_product_to_the_cart_with_not_default_quantity(self):

        self.assertEqual(self.cart, self.empty_cart)
        add_method = Cart.add(self, self.product, self.random_quantity_01)
        self.assertEqual(int(self.cart['1']['price']), self.product.price)
        self.assertEqual(self.cart['1']['quantity'], self.random_quantity_01)

    def test_add_product_to_the_cart_with_default_quantity_override_true(self):

        self.assertEqual(self.cart, self.empty_cart)
        add_method_01 = Cart.add(self, self.product, override_quantity=True)
        add_method_02 = Cart.add(self, self.product, override_quantity=True)
        self.assertEqual(int(self.cart['1']['price']), self.product.price)
        self.assertEqual(self.cart['1']['quantity'], self.default_quantity)

    def test_add_product_to_cart_with_not_default_quantity_override_true(self):

        self.assertEqual(self.cart, self.empty_cart)
        add_method_01 = Cart.add(self,
                                 self.product,
                                 self.random_quantity_01,
                                 override_quantity=True)

        self.assertEqual(int(self.cart['1']['price']), self.product.price)
        self.assertEqual(self.cart['1']['quantity'], self.random_quantity_01)

        add_method_02 = Cart.add(self,
                                 self.product,
                                 self.random_quantity_02,
                                 override_quantity=True)
        self.assertEqual(int(self.cart['1']['price']), self.product.price)
        self.assertEqual(self.cart['1']['quantity'], self.random_quantity_02)

    def test_add_product_to_cart_with_default_quantity_override_false(self):
        self.assertEqual(self.cart, self.empty_cart)
        add_method_01 = Cart.add(self, self.product)
        self.assertEqual(int(self.cart['1']['price']), self.product.price)
        self.assertEqual(self.cart['1']['quantity'], self.default_quantity)

        sum_quantity = self.default_quantity + self.default_quantity
        add_method_02 = Cart.add(self, self.product)
        self.assertEqual(int(self.cart['1']['price']), self.product.price)
        self.assertEqual(self.cart['1']['quantity'], sum_quantity)

    def test_add_product_to_cart_with_not_default_quantity_override_false(self):

        self.assertEqual(self.cart, self.empty_cart)
        add_method_01 = Cart.add(self,
                                 self.product,
                                 self.random_quantity_01)

        self.assertEqual(int(self.cart['1']['price']), self.product.price)
        self.assertEqual(self.cart['1']['quantity'], self.random_quantity_01)

        add_method_02 = Cart.add(self,
                                 self.product,
                                 self.random_quantity_02)
        sum_quantity = self.random_quantity_01 + self.random_quantity_02
        self.assertEqual(int(self.cart['1']['price']), self.product.price)
        self.assertEqual(self.cart['1']['quantity'], sum_quantity)

    def save(self):
        self.session.modified = True
