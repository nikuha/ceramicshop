from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    content = {}
    return render(request, 'basketapp/basket.html', content)


def add_product(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('authapp:login'))

    # product = get_object_or_404(Product, pk=pk)
    # basket = Basket.objects.filter(user=request.user, product=product).first()

    basket = request.user.basket.filter(product=pk).first()

    if not basket:
        basket = Basket(user=request.user, product_id=pk)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_product(request, pk):
    content = {}
    return render(request, 'basketapp/basket.html', content)
