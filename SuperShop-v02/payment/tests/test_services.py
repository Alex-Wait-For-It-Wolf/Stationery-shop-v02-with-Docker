from django.test import TestCase

from ..services import _get_list_of_products_from_the_order
from shop.models import Category, Product
from orders.models import Order, OrderItem


class GetListOfProductsFromTheOrderTests(TestCase):

    def setUp(self):
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

    def test_get_list_of_products_from_the_order(self):
        function_products = _get_list_of_products_from_the_order(self.order)
        test_products = [item.product for item in self.order.items.all()]
        self.assertEqual(function_products, test_products)

