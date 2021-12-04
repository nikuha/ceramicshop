from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product, Contact


def index(request):
    context = {
        'page_title': 'главная',
        'content_class': 'main-page',
        'main_path': main_path(request),
        'basket': get_basket(request)
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    categories = ProductCategory.objects.all()
    if pk:
        category = get_object_or_404(ProductCategory, id=pk)
        products = category.product_set.all()
    else:
        products = Product.objects.order_by('price').all()[:9]

    context = {
        'page_title': 'посуда',
        'categories': categories,
        'products': products,
        'category_id': pk,
        'main_path': main_path(request),
        'basket': get_basket(request)
    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk=None):
    categories = ProductCategory.objects.all()
    product = Product.objects.get(pk=pk)

    context = {
        'page_title': product.name,
        'categories': categories,
        'product': product,
        'category_id': product.category_id,
        'main_path': main_path(request),
        'basket': get_basket(request)
    }
    return render(request, 'mainapp/product.html', context)


def contacts(request):
    items = Contact.objects.all()
    context = {
        'page_title': 'контакты',
        'contacts': items,
        'main_path': main_path(request),
        'basket': get_basket(request)
    }
    return render(request, 'mainapp/contacts.html', context)


def get_basket(request):
    return request.user.is_authenticated and request.user.basket_set.all() or []


def handler404(request, exception=None):
    response = render(request, "mainapp/404.html")
    response.status_code = 404
    return response


def main_path(request):
    return ':'.join(request.resolver_match.namespaces) + ':' + request.resolver_match.url_name
