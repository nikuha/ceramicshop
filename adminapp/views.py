from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm
from adminapp.forms import AdminContactCreateForm, AdminProductCategoryCreateForm
from authapp.models import ShopUser
from mainapp.models import Contact, ProductCategory


@user_passes_test(lambda x: x.is_superuser)
def index(request):
    context = {
        'page_title': 'Админка'
    }
    return render(request, 'adminapp/index.html', context)


def products(request):
    pass


@user_passes_test(lambda x: x.is_superuser)
def categories(request):
    object_list = ProductCategory.objects.all().order_by('-is_active', 'pk')
    context = {
        'page_title': 'Админка / Категории продуктов',
        'object_list': object_list
    }
    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_create(request):
    if request.method == 'POST':
        category_form = AdminProductCategoryCreateForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        category_form = AdminProductCategoryCreateForm()

    context = {
        'page_title': 'Админка / Добавление категории продуктов',
        'update_form': category_form
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_update(request, pk):
    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        edit_form = AdminProductCategoryCreateForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_update', args=[edit_category.pk]))
    else:
        edit_form = AdminProductCategoryCreateForm(instance=edit_category)

    context = {
        'page_title': 'Админка / Редактирование категории продуктов',
        'update_form': edit_form
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        # category.delete()
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))

    context = {
        'page_title': 'Админка / Удаление категории продуктов',
        'category_to_delete': category
    }
    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_restore(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)

    category.is_active = True
    category.save()
    return HttpResponseRedirect(reverse('adminapp:categories'))


@user_passes_test(lambda x: x.is_superuser)
def contacts(request):
    object_list = Contact.objects.all().order_by('-is_active', 'pk')
    context = {
        'page_title': 'Админка / Контакты',
        'object_list': object_list
    }
    return render(request, 'adminapp/contacts.html', context)


@user_passes_test(lambda x: x.is_superuser)
def contact_create(request):
    if request.method == 'POST':
        contact_form = AdminContactCreateForm(request.POST, request.FILES)
        if contact_form.is_valid():
            contact_form.save()
            return HttpResponseRedirect(reverse('adminapp:contacts'))
    else:
        contact_form = AdminContactCreateForm()

    context = {
        'page_title': 'Админка / Добавление контакта',
        'update_form': contact_form
    }
    return render(request, 'adminapp/contact_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def contact_update(request, pk):
    edit_contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        edit_form = AdminContactCreateForm(request.POST, request.FILES, instance=edit_contact)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:contact_update', args=[edit_contact.pk]))
    else:
        edit_form = AdminContactCreateForm(instance=edit_contact)

    context = {
        'page_title': 'Админка / Редактирование контакта',
        'update_form': edit_form
    }
    return render(request, 'adminapp/contact_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if request.method == 'POST':
        # contact.delete()
        contact.is_active = False
        contact.save()
        return HttpResponseRedirect(reverse('adminapp:contacts'))

    context = {
        'page_title': 'Админка / Удаление контакта',
        'contact_to_delete': contact
    }
    return render(request, 'adminapp/contact_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def contact_restore(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    contact.is_active = True
    contact.save()
    return HttpResponseRedirect(reverse('adminapp:contacts'))


@user_passes_test(lambda x: x.is_superuser)
def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'page_title': 'Админка / Пользователи',
        'object_list': users_list
    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = AdminShopUserCreateForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = AdminShopUserCreateForm()

    context = {
        'page_title': 'Админка / Добавление пользователя',
        'update_form': user_form
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_update(request, pk):
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_user.pk]))
    else:
        edit_form = AdminShopUserUpdateForm(instance=edit_user)

    context = {
        'page_title': 'Админка / Редактирование пользователя',
        'update_form': edit_form
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))

    context = {
        'page_title': 'Админка / Удаление пользователя',
        'user_to_delete': user
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_restore(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse('adminapp:users'))
