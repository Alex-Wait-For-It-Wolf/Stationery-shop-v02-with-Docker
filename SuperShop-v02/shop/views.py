import redis

from django.conf import settings
from django.contrib.postgres.search import SearchVector, SearchQuery, \
                                           SearchRank, TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from loguru import logger

from .forms import SearchForm
from .models import Category, Product
from .recommender import Recommender
from cart.forms import CartAddProductForm


@logger.catch
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    object_list = (Product
                   .objects
                   .filter(available=True)
                   .order_by('translations__name'))
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        object_list = (object_list
                       .filter(available=True)
                       .filter(category=category)
                       .order_by('translations__name'))

    cart_product_form = CartAddProductForm()
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'cart_product_form': cart_product_form,
                   'page': page,})

@logger.catch
def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    try:
        r = Recommender()
        recommended_products = r.suggest_products_for([product], 4)
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Attention {e}")
        recommended_products = None

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                  'cart_product_form': cart_product_form,
                  'recommended_products': recommended_products})

@logger.catch
def product_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.filter(available=True).annotate(
                similarity=TrigramSimilarity('translations__name',
                                             query) + \
                           TrigramSimilarity('translations__description',
                                             query),
                      ).filter(similarity__gt=0.5).order_by('-similarity')
    return render(request,
                  'shop/product/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})

