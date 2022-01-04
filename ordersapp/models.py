from django.db import models
from django.conf import settings
from mainapp.models import Product


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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='статус', max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    @property
    def get_total_quantity(self):
        items = self.order_items.select_related('product')
        return sum(list(map(lambda x: x.quantity, items)))

    @property
    def get_total_cost(self):
        items = self.order_items.select_related('product')
        return sum(list(map(lambda x: x.get_product_cost, items)))

    def get_items(self):
        pass

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
    def get_product_cost(self):
        return self.product.price * self.quantity
