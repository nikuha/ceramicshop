from django.conf import settings
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from mainapp.models import Product
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem


class PageContextMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class OrderListView(PageContextMixin, ListView):
    model = Order
    page_title = 'Список заказов'

    def get_queryset(self):
        # return super().get_queryset().filter(is_active=True, user=self.request.user)
        return self.request.user.orders.filter(is_active=True)


class OrderCreateView(PageContextMixin, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    page_title = 'Создание заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = self.request.user.basket.all()
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=basket_items.count()+1)
                formset = OrderFormSet()
                for form, basket_item in zip(formset.forms, basket_items):
                    form.initial['product'] = basket_item.product
                    form.initial['quantity'] = basket_item.quantity
                    form.initial['price'] = basket_item.product.price
                basket_items.delete()
            else:
                formset = OrderFormSet()
        context['order_items'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                self.request.user.basket.all().delete()
                order_items.instance = self.object
                order_items.save()

        if self.object.total_cost == 0:
            self.object.delete()

        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(PageContextMixin, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    page_title = 'Создание заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['order_items'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']

        with transaction.atomic():
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()

            if self.object.total_cost == 0:
                self.object.delete()

        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(PageContextMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:list')
    page_title = 'Удаление заказа'


class OrderDetailView(PageContextMixin, DetailView):
    model = Order
    page_title = 'Просмотр заказа'


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('ordersapp:list'))


def get_product_price(request, pk):
    if request.is_ajax():
        item = get_object_or_404(Product, pk=pk)
        return JsonResponse({
            'price': str(round(item.price))
        })
    else:
        return JsonResponse({'error': 'Что-то пошло не так'})
