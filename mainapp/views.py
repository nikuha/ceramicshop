from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product, Contact


def index(request):
    context = {
        'page_title': 'главная',
        'content_class': 'main-page'
    }
    return render(request, 'mainapp/index.html', context)


def hot_products(request):
    categories = ProductCategory.objects.filter(is_active=True).order_by('pk')
    hot_product = Product.objects.filter(is_active=True, category__is_active=True).order_by('?').first()
    products = Product.objects.filter(category=hot_product.category, is_active=True).exclude(
        pk=hot_product.pk).order_by('?').all()[:3]

    context = {
        'page_title': 'посуда',
        'categories': categories,
        'products': products,
        'category_id': -1,
        'hot_product': hot_product
    }
    return render(request, 'mainapp/products_hot.html', context)


def pagination(request, objects):
    paginator = Paginator(objects, 6)
    page = request.GET['page'] if 'page' in request.GET else 1
    try:
        objects_paginator = paginator.page(page)
    except PageNotAnInteger:
        objects_paginator = paginator.page(1)
    except EmptyPage:
        objects_paginator = paginator.page(paginator.num_pages)
    return objects_paginator


def products(request, pk):
    categories = ProductCategory.objects.filter(is_active=True).order_by('pk')
    if pk:
        category = get_object_or_404(ProductCategory, id=pk)
        products = category.product_set.filter(is_active=True).order_by('pk')
    else:
        products = Product.objects.filter(is_active=True).order_by('-pk').all()

    products_paginator = pagination(request, products)

    context = {
        'page_title': 'посуда',
        'categories': categories,
        'products': products_paginator,
        'category_id': pk,
        'hot_product': None
    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk=None):
    categories = ProductCategory.objects.filter(is_active=True).order_by('pk')
    product = Product.objects.get(pk=pk)

    context = {
        'page_title': product.name,
        'categories': categories,
        'product': product,
        'category_id': product.category_id
    }
    return render(request, 'mainapp/product.html', context)


def contacts(request):
    items = Contact.objects.filter(is_active=True).order_by('pk')
    context = {
        'page_title': 'контакты',
        'contacts': items
    }
    return render(request, 'mainapp/contacts.html', context)


def handler404(request, exception=None):
    response = render(request, "mainapp/404.html")
    response.status_code = 404
    return response
