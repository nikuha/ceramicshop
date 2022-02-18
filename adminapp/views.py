from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from adminapp.forms import AdminUserCreateForm, AdminUserUpdateForm
from adminapp.forms import AdminContactCreateForm
from adminapp.forms import AdminProductCreateForm, AdminProductCategoryCreateForm
from authapp.models import User
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


class ToggleActiveMixin:

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.is_active = not object.is_active
        object.save()
        success_url = self.success_url or self.get_success_url()
        return HttpResponseRedirect(success_url)


class IndexView(SuperUserOnlyMixin, TemplateView):
    template_name = 'adminapp/index.html'
    page_title = 'Админка'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(is_active=True).order_by('-pk')
        context['products'] = Product.objects.filter(is_active=True).order_by('-pk')[:5]
        context['users'] = User.objects.filter(is_active=True).order_by('-pk')[:5]
        context['contacts'] = Contact.objects.filter(is_active=True).order_by('-pk')[:5]
        return context


class ProductListView(SuperUserOnlyMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 5

    def get_category(self):
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(ProductCategory, pk=pk)
        else:
            return ProductCategory.objects.filter(is_active=True).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.order_by('-is_active', 'pk').all()
        context['category'] = self.get_category()
        context['page_title'] = 'Админка / Продукты категории ' + context['category'].name
        return context

    def get_queryset(self, **kwargs):
        category = self.get_category()
        return category.product_set.order_by('-is_active', 'pk')


class ProductCreateView(SuperUserOnlyMixin, PageContextMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    page_title = 'Админка / Добавление продукта'
    form_class = AdminProductCreateForm

    # инициируем сразу нужную категорию
    def get_initial(self):
        initial = super(ProductCreateView, self).get_initial()
        initial['category'] = self.kwargs.get('pk')
        return initial

    # возвращаем в нужную категорию
    def get_success_url(self):
        return reverse('adminapp:category_products', kwargs={'pk': self.object.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_pk'] = self.kwargs.get('pk')
        return context


class ProductUpdateView(SuperUserOnlyMixin, PageContextMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    page_title = 'Админка / Редактирование продукта'
    form_class = AdminProductCreateForm

    def get_success_url(self):
        return reverse('adminapp:category_products', kwargs={'pk': self.object.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_pk'] = self.object.category.pk
        return context


class ProductToggleActiveView(SuperUserOnlyMixin, ToggleActiveMixin, DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('adminapp:category_products', args=[self.get_object().category_id])


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

    # def form_valid(self, form):
    #     discount = form.cleaned_data['discount']
    #     if discount:
    #         self.object.product_set.update(price=F('price') * (1 - discount / 100))
    #
    #     return super().form_valid(form)


class CategoryToggleActiveView(SuperUserOnlyMixin, ToggleActiveMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('adminapp:categories')


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


class ContactToggleActiveView(SuperUserOnlyMixin, ToggleActiveMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('adminapp:contacts')


class UserListView(SuperUserOnlyMixin, PageContextMixin, ListView):
    model = User
    template_name = 'adminapp/users.html'
    page_title = 'Админка / Пользователи'
    ordering = ['-is_active', 'pk']
    paginate_by = 5


class UserCreateView(SuperUserOnlyMixin, PageContextMixin, CreateView):
    model = User
    template_name = 'adminapp/user_update.html'
    page_title = 'Админка / Добавление пользователя'
    success_url = reverse_lazy('adminapp:users')
    form_class = AdminUserCreateForm


class UserUpdateView(SuperUserOnlyMixin, PageContextMixin, UpdateView):
    model = User
    template_name = 'adminapp/user_update.html'
    page_title = 'Админка / Редактирование пользователя'
    success_url = reverse_lazy('adminapp:users')
    form_class = AdminUserUpdateForm


class UserToggleActiveView(SuperUserOnlyMixin, ToggleActiveMixin, DeleteView):
    model = User
    success_url = reverse_lazy('adminapp:users')
