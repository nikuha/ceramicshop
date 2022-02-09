from django.db import models
from django.conf import settings

from mainapp.models import Product
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачено'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдачи'),
        (CANCEL, 'отмена заказа')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='статус', max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', db_index=True, default=True)

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    @property
    def is_forming(self):
        return self.status == self.FORMING

    @property
    def total_quantity(self):
        items = self.order_items.select_related('product')
        return sum(list(map(lambda x: x.quantity, items)))

    @property
    def total_cost(self):
        items = self.order_items.select_related('product')
        return sum(list(map(lambda x: x.product_cost, items)))

    @property
    def get_items(self):
        return self.order_items.select_related('product')

    def delete(self, using=None, keep_parents=False):
        for item in self.order_items.select_related('product'):
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)

    @property
    def get_products(self):
        return Product.objects.filter(is_active=True, category__is_active=True)\
            .select_related('category').order_by('category', 'name')


@receiver(pre_delete, sender=OrderItem)
def product_quantity_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


@receiver(pre_save, sender=OrderItem)
def product_quantity_save(sender, instance, **kwargs):
    if instance.pk:
        get_item = instance.get_item(int(instance.pk))
        instance.product.quantity -= instance.quantity - get_item.quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()
