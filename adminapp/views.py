from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from adminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm
from adminapp.forms import AdminContactCreateForm
from adminapp.forms import AdminProductCreateForm, AdminProductCategoryCreateForm
from authapp.models import ShopUser
from mainapp.models import Contact, ProductCategory, Product


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PageContextMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


def pagination(request, objects):
    paginator = Paginator(objects, 4)
    page = request.GET['page'] if 'page' in request.GET else 1
    try:
        objects_paginator = paginator.page(page)
    except PageNotAnInteger:
        objects_paginator = paginator.page(1)
    except EmptyPage:
        objects_paginator = paginator.page(paginator.num_pages)
    return objects_paginator


@user_passes_test(lambda x: x.is_superuser)
def index(request):
    context = {
        'page_title': 'Админка'
    }
    return render(request, 'adminapp/index.html', context)


@user_passes_test(lambda x: x.is_superuser)
def products(request, pk=None):
    if pk:
        category = get_object_or_404(ProductCategory, pk=pk)
    else:
        category = ProductCategory.objects.filter(is_active=True).first()

    categories = ProductCategory.objects.order_by('-is_active', 'pk').all()

    object_list = category.product_set.order_by('-is_active', 'pk')

    context = {
        'page_title': f'Админка / Продукты категории {category.name}',
        'object_list': pagination(request, object_list),
        'category': category,
        'categories': categories
    }
    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_create(request, pk):
    if request.method == 'POST':
        product_form = AdminProductCreateForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_products', args=[pk]))
    else:
        category = ProductCategory.objects.filter(pk=pk).first()
        product_form = AdminProductCreateForm(initial={'category': category})

    context = {
        'page_title': 'Админка / Добавление продукта',
        'update_form': product_form,
        'category_pk': pk
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_update(request, pk):
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = AdminProductCreateForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:product_update', args=[edit_product.pk]))
    else:
        edit_form = AdminProductCreateForm(instance=edit_product)

    context = {
        'page_title': 'Админка / Редактирование продукта',
        'update_form': edit_form,
        'category_pk': edit_product.category_id
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_toggle_active(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = not product.is_active
        product.save()
    return HttpResponseRedirect(reverse('adminapp:category_products', args=[product.category_id]))


class ProductCategoryListView(SuperUserOnlyMixin, PageContextMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    page_title = 'Админка / Категории продуктов'
    ordering = ['-is_active', 'pk']


class ProductCategoryCreateView(SuperUserOnlyMixin, PageContextMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    page_title = 'Админка / Добавление категории продуктов'
    success_url = reverse_lazy('adminapp:categories')
    form_class = AdminProductCategoryCreateForm


class ProductCategoryUpdateView(SuperUserOnlyMixin, PageContextMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    page_title = 'Админка / Редактирование категории продуктов'
    success_url = reverse_lazy('adminapp:categories')
    form_class = AdminProductCategoryCreateForm
    # def get_success_url(self):
    #     return reverse('adminapp:category_update', kwargs={'pk': self.object.pk})


@user_passes_test(lambda x: x.is_superuser)
def category_toggle_active(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_active = not category.is_active
        category.save()
    return HttpResponseRedirect(reverse('adminapp:categories'))


class ContactListView(SuperUserOnlyMixin, PageContextMixin, ListView):
    model = Contact
    template_name = 'adminapp/contacts.html'
    page_title = 'Админка / Контакты'
    ordering = ['-is_active', 'pk']


class ContactCreateView(SuperUserOnlyMixin, PageContextMixin, CreateView):
    model = Contact
    template_name = 'adminapp/contact_update.html'
    page_title = 'Админка / Добавление контакта'
    success_url = reverse_lazy('adminapp:contacts')
    form_class = AdminContactCreateForm


class ContactUpdateView(SuperUserOnlyMixin, PageContextMixin, UpdateView):
    model = Contact
    template_name = 'adminapp/contact_update.html'
    page_title = 'Админка / Редактирование контакта'
    success_url = reverse_lazy('adminapp:contacts')
    form_class = AdminContactCreateForm


@user_passes_test(lambda x: x.is_superuser)
def contact_toggle_active(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if request.method == 'POST':
        contact.is_active = not contact.is_active
        contact.save()
    return HttpResponseRedirect(reverse('adminapp:contacts'))


class ShopUserListView(SuperUserOnlyMixin, PageContextMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    page_title = 'Админка / Пользователи'
    ordering = ['-is_active', 'pk']
    paginate_by = 5


class ShopUserCreateView(SuperUserOnlyMixin, PageContextMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    page_title = 'Админка / Добавление пользователя'
    success_url = reverse_lazy('adminapp:users')
    form_class = AdminShopUserCreateForm


class ShopUserUpdateView(SuperUserOnlyMixin, PageContextMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    page_title = 'Админка / Редактирование пользователя'
    success_url = reverse_lazy('adminapp:users')
    form_class = AdminShopUserUpdateForm


@user_passes_test(lambda x: x.is_superuser)
def user_toggle_active(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
    return HttpResponseRedirect(reverse('adminapp:users'))