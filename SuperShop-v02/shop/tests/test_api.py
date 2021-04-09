from django.urls import reverse
from rest_framework.test import APITestCase

from ..factories import CategoryFactory, ProductFactory


class CategoryListTests(APITestCase):

    def setUp(self):
        self.category_01 = CategoryFactory()
        self.category_02 = CategoryFactory()
        self.category_03 = CategoryFactory()

    def test_category_list_contains_categories(self):
        url = reverse('api_shop:category_list')
        response = self.client.get(url)
        self.assertContains(response, self.category_01)
        self.assertContains(response, self.category_02)
        self.assertContains(response, self.category_03)
        self.assertNotContains(response, 'something not from response')
        self.assertEqual(response.status_code, 200)


class ProductListTests(APITestCase):

    def setUp(self):
        self.product_01 = ProductFactory()
        self.product_02 = ProductFactory()
        self.product_03 = ProductFactory()

    def test_product_list_contains_products(self):
        url = reverse('api_shop:product_list')
        response = self.client.get(url)
        self.assertContains(response, self.product_01)
        self.assertContains(response, self.product_02)
        self.assertContains(response, self.product_03)
        self.assertNotContains(response, 'something not from response')
        self.assertEqual(response.status_code, 200)


class ProductDetailTests(APITestCase):

    def setUp(self):
        self.product_01 = ProductFactory()
        self.product_02 = ProductFactory()
        self.product_03 = ProductFactory()

    def test_product_detail_contains_product(self):
        url = reverse('api_shop:product_detail', args=(self.product_01.id,))
        response = self.client.get(url)
        self.assertContains(response, self.product_01)
        self.assertNotContains(response, 'something not from response')
        self.assertEqual(response.status_code, 200)
