from django.db import models

from authapp.models import ShopUser
from ceramicshop import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(verbose_name='количество', default=1)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)
