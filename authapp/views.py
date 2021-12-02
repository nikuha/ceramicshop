from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopRegisterForm, ShopUserEditForm


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('mainapp:index'))
    if request.method == 'POST':
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('mainapp:index'))
    else:
        login_form = ShopUserLoginForm()

    content = {'page_title': 'Вход', 'login_form': login_form, 'main_path': main_path(request)}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('authapp:login'))


def register(request):
    if request.method == 'POST':
        register_form = ShopRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        register_form = ShopRegisterForm()

    content = {'page_title': 'Регистрация', 'register_form': register_form, 'main_path': main_path(request)}
    return render(request, 'authapp/register.html', content)


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    content = {'page_title': 'Редактирование', 'edit_form': edit_form, 'main_path': main_path(request)}
    return render(request, 'authapp/edit.html', content)


def main_path(request):
    return ':'.join(request.resolver_match.namespaces) + ':' + request.resolver_match.url_name
