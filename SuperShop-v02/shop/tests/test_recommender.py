import redis
from operator import itemgetter
from django.conf import settings
from django.test import TestCase

from ..factories import ProductFactory
from ..recommender import Recommender


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class RecommenderTests(TestCase):

    def setUp(self):
        self.product_01 = ProductFactory(
            name='Bakolat',
        )
        self.product_02 = ProductFactory(
            name='Makolato'
        )
        self.product_03 = ProductFactory(
            name='Kwakukata',
        )
        self.empty_p_list = []
        self.product_list = [self.product_01, self.product_02, self.product_03]
        self.list_p_01 = [self.product_01]
        self.list_p_02 = [self.product_02]
        self.list_p_03 = [self.product_03]

        self.recom = Recommender()
        self.recom.products_bought(self.product_list)


    def test_get_product_key(self):
        product_key = self.recom.get_product_key(self.product_01.id)
        returned_data = f'product:{self.product_01.id}:purchased_with'
        self.assertEqual(product_key, returned_data)

    def test_suggest_products_for_products_len_equal_zero(self):
        suggest_products = self.recom.suggest_products_for(self.empty_p_list)
        self.assertEqual(suggest_products, None)

    def test_suggest_products_for_products_len_equal_one(self):
        suggested_p_01 = self.recom.suggest_products_for(self.list_p_01)
        suggested_p_02 = self.recom.suggest_products_for(self.list_p_02)
        suggested_p_03 = self.recom.suggest_products_for(self.list_p_03)

        self.assertEqual(suggested_p_01,
                         list(itemgetter(2,1)(self.product_list)))
        self.assertEqual(suggested_p_02,
                         list(itemgetter(2,0)(self.product_list)))
        self.assertEqual(suggested_p_03,
                         list(itemgetter(1,0)(self.product_list)))

        # User r.flushdb() or clear_purchases() basically they do same thing
        # clear redis db of recommendations.
        #r.flushdb()
        self.recom.clear_purchases()

    def test_suggest_products_for_products_len_more_than_one(self):
        product_01_and_02 = [self.product_01, self.product_02]
        product_01_and_03 = [self.product_01, self.product_03]
        product_02_and_03 = [self.product_02, self.product_03]

        suggested_p_01 = self.recom.suggest_products_for(product_01_and_02)
        suggested_p_02 = self.recom.suggest_products_for(product_01_and_03)
        suggested_p_03 = self.recom.suggest_products_for(product_02_and_03)

        self.assertEqual(suggested_p_01, self.list_p_03)
        self.assertEqual(suggested_p_02, self.list_p_02)
        self.assertEqual(suggested_p_03, self.list_p_01)

        self.recom.clear_purchases()

        suggested_p_04 = self.recom.suggest_products_for(product_01_and_02)
        self.assertEqual(suggested_p_04, self.empty_p_list)
