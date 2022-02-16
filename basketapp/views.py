from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from basketapp.models import Basket


class UserOnlyMixin:
    @method_decorator(user_passes_test(lambda x: x.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PageContextMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class BasketView(UserOnlyMixin, PageContextMixin, TemplateView):
    template_name = 'basketapp/basket.html'
    page_title = 'Корзина'


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
        quantity_diff = quantity - basket_record.quantity
        if quantity >= 1 and quantity_diff <= basket_record.product.quantity:
            # basket_record.quantity = quantity
            basket_record.quantity = F('quantity') + quantity_diff
            basket_record.save()
            # print_queries('UPDATE', connection.queries)
            basket_record.refresh_from_db()
        return JsonResponse({
            'product_cost': str(round(basket_record.product_cost)) + '&nbsp;' + settings.CURRENCY_SYMBOL,
            'total_quantity': request.user.basket_total_quantity,
            'total_cost': str(round(request.user.basket_total_cost)) + '&nbsp;' + settings.CURRENCY_SYMBOL,
            'product_quantity': basket_record.product.quantity
        })
    else:
        return JsonResponse({'error': 'Что-то пошло не так'})


def print_queries(q_type, queries):
    for query in filter(lambda x: q_type in x['sql'], queries):
        print(query['sql'])
