from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm
from authapp.models import ShopUser


@user_passes_test(lambda x: x.is_superuser)
def index(request):
    context = {
        'page_title': 'Админка'
    }
    return render(request, 'adminapp/index.html', context)


def categories(request):
    pass


def products(request):
    pass


def contacts(request):
    pass


def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'page_title': 'Админка / Пользователи',
        'object_list': users_list
    }
    return render(request, 'adminapp/users.html', context)


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


def user_restore(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse('adminapp:users'))

