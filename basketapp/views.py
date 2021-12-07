from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    content = {
        'page_title': 'Корзина',
        'basket': request.user.basket.order_by('product__category').all()
    }
    return render(request, 'basketapp/basket.html', content)


@login_required
def add_product(request, pk):
    # product = get_object_or_404(Product, pk=pk)
    # basket = Basket.objects.filter(user=request.user, product=product).first()

    basket = request.user.basket.filter(product=pk).first()

    if not basket:
        basket = Basket(user=request.user, product_id=pk)

    basket.quantity += 1
    basket.save()

    if 'login' in request.META.get('HTTP_REFERER'):
        url = reverse('mainapp:products:product', args=[pk])
    else:
        url = request.META.get('HTTP_REFERER')

    return HttpResponseRedirect(url)


@login_required
def remove_product(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

