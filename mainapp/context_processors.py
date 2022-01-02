# для удобного получения полного пути, где мы находимся и формирования класса active для ссылок
from mainapp.models import ProductCategory


def main_path(request):
    return {
        'main_path': ':'.join(request.resolver_match.namespaces) + ':' + request.resolver_match.url_name
    }


def basket(request):
    baskets_list = []
    if request.user.is_authenticated:
        baskets_list = request.user.basket.order_by('product__category').all()
    return {
        'basket': baskets_list
    }


def sorted_categories(request):
    categories = ProductCategory.objects.filter(is_active=True).order_by('pk')
    return {
        'sorted_categories': categories
    }
