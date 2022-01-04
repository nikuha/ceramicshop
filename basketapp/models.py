from django.db import models
from django.urls import reverse

from authapp.models import User
from django.conf import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        # return sum([x.quantity for x in self.user.basket.all()])
        return sum(self.user.basket.values_list('quantity', flat=True))

    @property
    def total_cost(self):
        return sum([x.product_cost for x in self.user.basket.all()])

    @property
    def remove_from_basket_url(self):
        return reverse('basketapp:remove', kwargs={'pk': self.id})
