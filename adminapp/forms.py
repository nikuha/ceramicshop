from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
import django.forms as forms

from authapp.models import User
from mainapp.models import Contact, ProductCategory, Product


class AdminUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'is_superuser', 'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field_name
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("У нас сторого 18+!")
        return data


class AdminUserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('is_superuser', 'username', 'password', 'email', 'first_name', 'last_name', 'age', 'avatar')

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


class AdminContactCreateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('city', 'phone', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field_name
            field.help_text = ''


class AdminProductCategoryCreateForm(forms.ModelForm):
    discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field_name
            field.help_text = ''


class AdminProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'description', 'price', 'quantity', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field_name
            field.help_text = ''
