from django import template
from ..forms import SearchForm
register = template.Library()


@register.inclusion_tag('shop/product/search_form.html')
def search_form_tag():
    return {'form': SearchForm()}

