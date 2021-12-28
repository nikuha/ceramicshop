from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from authapp.mixin import PageContextMixin
from authapp.models import ShopUser


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('mainapp:index'))

    if 'next' in request.GET.keys():
        next_url = request.GET['next']
    elif 'next' in request.POST.keys():
        next_url = request.POST['next']
    else:
        next_url = ''

    if request.method == 'POST':
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if not next_url:
                    next_url = reverse('mainapp:index')
                return HttpResponseRedirect(next_url)
    else:
        login_form = ShopUserLoginForm()

    content = {'page_title': 'Вход', 'login_form': login_form, 'main_path': main_path(request), 'next_url': next_url}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('authapp:login'))


class RegisterShopUserView(FormView, PageContextMixin):
    model = ShopUser
    template_name = 'authapp/register.html'
    page_title = 'Регистрация'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('authapp:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'page_title': self.page_title})

    def verify(self, email, activate_key):
        try:
            user = ShopUser.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user)
            return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))

    @staticmethod
    def send_verify_link(user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


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
