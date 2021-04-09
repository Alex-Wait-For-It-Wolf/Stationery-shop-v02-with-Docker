from datetime import datetime

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from freezegun import freeze_time


from ..models import Category, Product


class CategoryTest(TestCase):

    def setUp(self):
        self.category_fruits = Category.objects.create(
            name='Fruits',
            slug='fruits',
        )

        self.category_vegatables = Category.objects.create(
            name='Vegetable',
            slug='vegetable',
        )

        self.category_berrys = Category.objects.create(
            name='Berrys',
            slug='berrys',
        )

    def test_category_listing(self):
        self.assertEqual(f'{self.category_fruits.name}', 'Fruits')
        self.assertEqual(f'{self.category_fruits.slug}', 'fruits')


class ProductTest(TestCase):
    
    @freeze_time('2021-01-30 14:05:20.232678+00:00')
    def setUp(self):
        self.category_fruits = Category.objects.create(name='Fruits',
                                                       slug='fruits')

        self.category_vegatables = Category.objects.create(name='Vegetables',
                                                           slug='vegetables')

        self.category_berrys = Category.objects.create(name='Berrys',
                                                       slug='berrys')

        self.product_banana = Product.objects.create(
            name='Banana', 
            slug='banana',
            description='some banana',
            category=self.category_fruits,
            image='123banana.jpg',
            price='25.00',
            available=True,
            created='added_automatically',
            updated='added_automatically',
        )

        self.product_carrot = Product.objects.create(
            name='Carrot', 
            slug='carrot',
            description='some carrot',
            category=self.category_vegatables,
            image='123carrot.jpg',
            price='26.00',
            available=True,
            created='added_automatically',
            updated='added_automatically',
        )
        
        self.product_strawberry = Product.objects.create(
            name='Strawberry', 
            slug='strawberry',
            description='some strawberry',
            category=self.category_berrys,
            image='123strawberry.jpg',
            price='27.00',
            available=True,
            created='added_automatically',
            updated='added_automatically',
        )

        self.freezed_time = '2021-01-30 14:05:20.232678+00:00'

    def test_product_listing(self):
        self.assertEqual(f'{self.product_banana.name}', 'Banana')
        self.assertEqual(f'{self.product_banana.slug}', 'banana')
        self.assertEqual(f'{self.product_banana.description}', 'some banana')
        self.assertEqual(f'{self.product_banana.category}', 
                         self.category_fruits.name)
        self.assertEqual(f'{self.product_banana.image}', '123banana.jpg')
        self.assertEqual(f'{self.product_banana.price}', '25.00')
        self.assertEqual(f'{self.product_banana.available}', 'True')
        self.assertEqual(f'{self.product_banana.created}', self.freezed_time)
        self.assertEqual(f'{self.product_banana.updated}', self.freezed_time)


    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Banana')
        self.assertTemplateUsed(response, 'shop/product/list.html')

    def test_product_list_view_with_category_slag(self):
        response = self.client.get('/en/fruits/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fruits')
        self.assertContains(response, 'Banana')
        self.assertNotContains(response, 'Carrot')
        self.assertNotContains(response, 'Strawberry')
        self.assertTemplateUsed(response, 'shop/product/list.html')

    def test_product_list_view_without_category_slag(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fruits')
        self.assertContains(response, 'Vegetables')
        self.assertContains(response, 'Berrys')
        self.assertContains(response, 'Banana')
        self.assertContains(response, 'Carrot')
        self.assertContains(response, 'Strawberry')
        self.assertContains(response, 'Products')
        self.assertTemplateUsed(response, 'shop/product/list.html')

    def test_product_detail_view(self):
        response = self.client.get(self.product_banana.get_absolute_url())
        no_response = self.client.get('/en/12/no-banana/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Banana')
        self.assertTemplateUsed(response, 'shop/product/detail.html')
