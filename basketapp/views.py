from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
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
    basket_record = request.user.basket.filter(product=pk).first()

    if not basket_record:
        basket_record = Basket(user=request.user, product_id=pk)

    if basket_record.quantity + 1 <= basket_record.product.quantity:
        basket_record.quantity += 1
        basket_record.save()

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


@login_required
def update_quantity(request, pk):
    if request.is_ajax():
        basket_record = get_object_or_404(Basket, pk=pk)
        quantity = int(request.GET['quantity'])
        if quantity <= basket_record.product.quantity:
            basket_record.quantity = quantity
            basket_record.save()
        # result = render_to_string('basketapp/includes/inc_basket_list.html', content)
        return JsonResponse({
            'product_cost': round(basket_record.product_cost),
            'total_quantity': round(basket_record.total_quantity),
            'total_cost': round(basket_record.total_cost)
        })
    else:
        return JsonResponse({'error': 'Что-то пошло не так'})
