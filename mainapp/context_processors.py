from mainapp.models import ProductCategory
from django.conf import settings
from django.core.cache import cache


def main_path(request):
    return {
        'main_path': ':'.join(request.resolver_match.namespaces) + ':' + request.resolver_match.url_name
    }


def basket(request):
    baskets_list = []
    if request.user.is_authenticated:
        baskets_list = request.user.basket.select_related('product').order_by('product__category').all()
    return {
        'basket': baskets_list
    }


def sorted_categories(request):
    if settings.LOW_CACHE:
        key = 'categories'
        categories = cache.get(key)
        if categories is None:
            categories = ProductCategory.objects.filter(is_active=True).order_by('pk')
            cache.set(key, categories)
    else:
        categories = ProductCategory.objects.filter(is_active=True).order_by('pk')
    return {
        'sorted_categories': categories
    }
