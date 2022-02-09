from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from mainapp.models import ProductCategory, Product, Contact
from django.conf import settings
from django.core.cache import cache


def get_categories(params):
    return ProductCategory.objects.filter(is_active=True).order_by('pk')


def get_category_products(params):
    return Product.objects.filter(is_active=True, category_id=params).order_by('pk')


def get_cached_queryset(key, get_function, params=None):
    if settings.LOW_CACHE:
        categories = cache.get(key)
        if categories is None:
            categories = get_function(params)
            cache.set(key, categories)
    else:
        categories = get_function(params)
    return categories


class PageContextMixin:
    page_title = ''
    category_id = 0
    show_categories = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['category_id'] = self.category_id
        if self.show_categories:
            context['sorted_categories'] = get_cached_queryset('categories', get_categories)
        return context


class IndexView(PageContextMixin, TemplateView):
    template_name = 'mainapp/index.html'
    page_title = 'Главная'
    show_categories = False


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


class AllProductsView(PageContextMixin, ListView):
    model = Product
    template_name = 'mainapp/products.html'
    page_title = 'посуда'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(is_active=True, category__is_active=True).order_by('-pk')


class ProductsView(PageContextMixin, ListView):
    model = Product
    template_name = 'mainapp/products.html'
    page_title = 'посуда'

    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']
        self.category_id = pk
        return get_cached_queryset(f'products{pk}', get_category_products, pk)


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
    show_categories = False

    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(is_active=True).order_by('pk')


def handler404(request, exception=None):
    response = render(request, "mainapp/404.html")
    response.status_code = 404
    return response
