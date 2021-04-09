from django.urls import path
from . import views

app_name = 'api_shop'

urlpatterns = [
    path('categories/',
         views.CategoryListView.as_view(),
         name='category_list'),

    path('products/',
         views.ProductListView.as_view(),
         name='product_list'),
    path('products/<pk>/',
         views.ProductDetailView.as_view(),
         name='product_detail'),
]
