from django.urls import reverse, resolve
from django.test import TestCase


class ProductListWithoutCategorySlugTests(TestCase):

    def test_product_list_without_category_slug(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertContains(response, 'Products')
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')


class ProductListWithCategorySlugTests(TestCase):

    def test_product_list_with_category_slug(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertContains(response, 'Products')
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')


class ProductDetailTests(TestCase):

    def test_homepage_template(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertContains(response, 'Products')
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')
