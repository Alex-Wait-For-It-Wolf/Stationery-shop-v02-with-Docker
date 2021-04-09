from django.test import TestCase
from django.urls import reverse, resolve

import json

from shop.factories import ProductFactory
from ..forms import CartAddProductForm



class CartAddProductFormTests(TestCase):

    def test_cart_add_valid_quantity(self):
        form_data_01 = {'quantity': 3, 'override': False}
        form_data_02 = {'quantity': 5, 'override': False}
        form_data_03 = {'quantity': 18, 'override': False}

        form_01 = CartAddProductForm(data=form_data_01)
        form_02 = CartAddProductForm(data=form_data_02)
        form_03 = CartAddProductForm(data=form_data_03)

        self.assertTrue(form_01.is_valid())
        self.assertTrue(form_02.is_valid())
        self.assertTrue(form_03.is_valid())

    def test_cart_add_invalid_quantity(self):

        form_data_01 = {'quantity': 21, 'override': False}
        form = CartAddProductForm(data=form_data_01)
        self.assertFalse(form.is_valid())
