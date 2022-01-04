from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
import django.forms as forms

from authapp.models import User, UserProfile


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field_name


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field_name
            field.help_text = ''

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        user.set_activation_key()
        user.save()
        return user

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("У нас сторого 18+!")
        return data


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.widget = forms.HiddenInput()
            else:
                field.widget.attrs['class'] = field_name
                field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("У нас сторого 18+!")
        return data


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    # def __init__(self, *args, **kwargs):
    #     super(UserEditForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         if field_name != 'gender':
    #             field.widget.attrs['class'] = 'form-control py-4'
    #         else:
    #             field.widget.attrs['class'] = 'form-control'
