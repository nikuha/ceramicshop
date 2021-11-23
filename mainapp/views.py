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


def products(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()

    context = {
        'page_title': 'посуда',
        'categories': categories,
        'products': products,
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
        'main_path': main_path(request)
    }
    return render(request, 'mainapp/product.html', context)


def contacts(request):
    # загрузить в базу контакты из файла
    # load_contacts_from_file()
    items = Contact.objects.all()
    context = {
        'page_title': 'контакты',
        'contacts': items,
        'main_path': main_path(request)
    }
    return render(request, 'mainapp/contacts.html', context)


def load_contacts_from_file():
    with open('mainapp/data/contacts.json') as json_file:
        items = json.load(json_file)
        for contact in items:
            new_contact = Contact(city=contact['city'], phone=contact['phone'], email=contact['email'])
            new_contact.save()


def main_path(request):
    return ':'.join(request.resolver_match.namespaces) + ':' + request.resolver_match.url_name
