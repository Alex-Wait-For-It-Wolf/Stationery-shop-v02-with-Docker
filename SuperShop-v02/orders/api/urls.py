from django.urls import path
from rest_framework import routers

from . import views


app_name = 'api_orders'

urlpatterns = [
    path('order_list/',
         views.OrderListView.as_view(),
         name='order_list'),
]
