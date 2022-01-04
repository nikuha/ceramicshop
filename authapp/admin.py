from django.contrib import admin
from authapp.models import User
from basketapp.admin import BasketAdmin
from basketapp.models import Basket


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = Basket
    inlines = (BasketAdmin,)
