from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from mainapp.models import ProductCategory, Product, Contact


class PageContextMixin:
    page_title = ''
    category_id = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['category_id'] = self.category_id
        return context


class IndexView(PageContextMixin, TemplateView):
    template_name = 'mainapp/index.html'
    page_title = 'Главная'


class HotProductsView(PageContextMixin, ListView):
    model = Product
    template_name = 'mainapp/products_hot.html'
    page_title = 'посуда'
    category_id = -1
    hot_product = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hot_product'] = self.hot_product
        return context

    def get_queryset(self, **kwargs):
        self.hot_product = Product.objects.filter(is_active=True, category__is_active=True).order_by('?').first()
        qs = super().get_queryset()
        products = qs.filter(category=self.hot_product.category, is_active=True).exclude(
            pk=self.hot_product.pk).order_by('?').all()[:3]
        return products


class ProductsView(PageContextMixin, ListView):
    model = Product
    template_name = 'mainapp/products.html'
    page_title = 'посуда'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        pk = self.kwargs['pk']
        if pk:
            category = get_object_or_404(ProductCategory, id=pk, is_active=True)
            qs = qs.filter(is_active=True, category=category).order_by('pk')
            self.category_id = pk
        else:
            qs = qs.filter(is_active=True).order_by('-pk').all()
        return qs


class ProductView(DetailView):
    model = Product
    template_name = 'mainapp/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cur_object = self.get_object()
        context['page_title'] = cur_object.name
        context['category_id'] = cur_object.category_id
        return context

    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(is_active=True)


class ContactsView(PageContextMixin, ListView):
    model = Contact
    template_name = 'mainapp/contacts.html'
    page_title = 'контакты'

    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(is_active=True).order_by('pk')


def handler404(request, exception=None):
    response = render(request, "mainapp/404.html")
    response.status_code = 404
    return response
