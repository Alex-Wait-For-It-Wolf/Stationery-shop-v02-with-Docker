from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from ..admin import export_to_csv, OrderAdmin, order_detail, order_pdf
from ..factories import OrderFactory
from ..models import Order


class ExportToSCVTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.order = OrderFactory()
        self.site = AdminSite()

    def test_export_to_scv_post(self):
        order = self.order
        modeladmin = OrderAdmin(Order, self.site)
        request = self.factory.post('/en/admin/orders/order/')
        queryset = Order.objects.filter(id=order.id)

        response = export_to_csv(modeladmin, request, queryset)
        response.client = Client()

        order_info = (f'{order.first_name},{order.last_name},{order.email}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order_info)
        self.assertNotContains(response,
                           'Hi there! I should not be on the page.')


class OrderDetailTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_order_detail(self):
        order = OrderFactory()
        response = order_detail(order)
        url = reverse('orders:admin_order_detail', args=[order.id])
        label = 'View'
        complete_url = f'<a href="{url}">{label}</a>'
        self.assertEqual(response, complete_url)


class OrderPDFTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_order_PDF(self):
        order = OrderFactory()
        response = order_pdf(order)
        url = reverse('orders:admin_order_pdf', args=[order.id])
        label = 'PDF'
        complete_url = f'<a href="{url}">{label}</a>'
        self.assertEqual(response, complete_url)
