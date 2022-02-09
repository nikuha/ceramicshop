from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from authapp.models import User
from django.conf import settings
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):
    def delete(self):
        for item in self:
            item.update_product_quantity('delete')
        super(BasketQuerySet, self).delete()


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @cached_property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def remove_from_basket_url(self):
        return reverse('basketapp:remove', kwargs={'pk': self.id})

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    def update_product_quantity(self, mode):
        if mode == 'create':
            self.product.quantity -= self.quantity
        elif mode == 'delete':
            self.product.quantity += self.quantity
        else:
            get_item = self.get_item(int(self.pk))
            self.product.quantity -= self.quantity - get_item.quantity
        self.product.save()

    def delete(self, using=None, keep_parents=False):
        self.update_product_quantity('delete')
        super(Basket, self).delete()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        mode = 'update' if self.pk else 'create'
        self.update_product_quantity(mode)
        super(Basket, self).save()
