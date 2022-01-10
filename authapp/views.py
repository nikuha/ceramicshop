from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, UpdateView

from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm, UserProfileEditForm
from authapp.mixin import PageContextMixin
from authapp.models import User


class UserOnlyMixin:
    @method_decorator(user_passes_test(lambda x: x.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserLoginView(LoginView, PageContextMixin):
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    page_title = 'Авторизация'

    def get_success_url(self):
        if 'next' in self.request.GET.keys() and self.request.GET['next']:
            return self.request.GET['next']
        elif 'next' in self.request.POST.keys() and self.request.POST['next']:
            return self.request.POST['next']
        return settings.LOGIN_REDIRECT_URL


class UserLogoutView(LogoutView):
    template_name = 'mainapp/index.html'


class UserRegisterView(FormView, PageContextMixin):
    model = User
    template_name = 'authapp/register.html'
    page_title = 'Регистрация'
    form_class = UserRegisterForm
    success_url = reverse_lazy('authapp:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user.send_verify_link():
                return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'page_title': self.page_title})

    def verify(self, email, activate_key):
        try:
            user = User.objects.get(email=email)
            if user.check_activation_key(activate_key):
                auth.login(self, user)
            return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('mainapp:index'))


class ProfileUpdateView(UserOnlyMixin, PageContextMixin, UpdateView):
    template_name = 'authapp/edit.html'
    page_title = 'Админка / Редактирование профиля'
    form_class = UserEditForm
    success_url = reverse_lazy('authapp:edit')

    def post(self, request, *args, **kwargs):
        form = UserEditForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
        return redirect(self.success_url)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context
