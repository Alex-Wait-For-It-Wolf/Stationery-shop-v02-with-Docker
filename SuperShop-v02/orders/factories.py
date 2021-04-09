import factory
from . import models

from shop.factories import ProductFactory


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Order

    first_name = 'John'
    last_name = 'Doe'
    email = 'johndoe@inabox.com'
    address = 'Sunset Blv 17'
    postal_code = 45345
    city = 'Miami'
    created = 'auto'
    updated = 'auto'
    paid = False
    braintree_id = '2sr455xjv2xf3css'
    coupon = None
    discount = 0
    payer = None


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    price = 25
    quantity = 3
