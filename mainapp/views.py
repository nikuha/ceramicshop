import json

from django.shortcuts import render
from mainapp.models import ProductCategory, Product, Contact


def index(request):
    context = {
        'page_title': 'главная',
        'content_class': 'main-page',
        'main_path': main_path(request)
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()

    context = {
        'page_title': 'посуда',
        'categories': categories,
        'products': products,
        'category_id': pk,
        'main_path': main_path(request)
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
        'main_path': main_path(request)
    }
    return render(request, 'mainapp/product.html', context)


def contacts(request):
    items = Contact.objects.all()
    context = {
        'page_title': 'контакты',
        'contacts': items,
        'main_path': main_path(request)
    }
    return render(request, 'mainapp/contacts.html', context)


def main_path(request):
    return ':'.join(request.resolver_match.namespaces) + ':' + request.resolver_match.url_name
