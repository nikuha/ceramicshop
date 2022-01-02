from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, UpdateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from authapp.mixin import PageContextMixin
from authapp.models import ShopUser


class UserOnlyMixin:
    @method_decorator(user_passes_test(lambda x: x.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class LoginView(LoginView, PageContextMixin):
    template_name = 'authapp/login.html'
    form_class = ShopUserLoginForm
    page_title = 'Авторизация'

    def get_success_url(self):
        if 'next' in self.request.GET.keys() and self.request.GET['next']:
            return self.request.GET['next']
        elif 'next' in self.request.POST.keys() and self.request.POST['next']:
            return self.request.POST['next']
        return settings.LOGIN_REDIRECT_URL


class LogoutView(LogoutView):
    template_name = 'mainapp/index.html'


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
        # return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
        user.email_user(subject, message, settings.EMAIL_HOST_USER, fail_silently=False)
        return True


class ProfileUpdateView(UserOnlyMixin, PageContextMixin, UpdateView):
    model = ShopUser
    template_name = 'authapp/edit.html'
    page_title = 'Админка / Редактирование профиля'
    form_class = ShopUserEditForm
    success_url = reverse_lazy('authapp:edit')

    def get_object(self, *args, **kwargs):
        return get_object_or_404(ShopUser, pk=self.request.user.pk)
