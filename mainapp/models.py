from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.templatetags.static import static
from django.db import connection


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя категории', max_length=64)
    description = models.TextField(verbose_name='описание категории', blank=True)
    is_active = models.BooleanField(verbose_name='активная', db_index=True, default=1)

    def __str__(self):
        return self.name

    @property
    def url(self):
        return reverse('mainapp:products:category', kwargs={'pk': self.id})


@receiver(post_save, sender=ProductCategory)
def save_category(sender, instance, created, **kwargs):
    instance.product_set.update(is_active=instance.is_active)
    # for query in filter(lambda x: 'UPDATE' in x['sql'], connection.queries):
    #     print(query['sql'])


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default=1)
    image = models.ImageField(upload_to='products_images', blank=True)
    is_active = models.BooleanField(verbose_name='активная', db_index=True, default=1)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    @property
    def url(self):
        return reverse('mainapp:products:product', kwargs={'pk': self.id})

    @property
    def image_or_default(self):
        return self.image.url if self.image else static('img/default.png')

    @property
    def add_to_basket_url(self):
        return reverse('basketapp:add', kwargs={'pk': self.id})

    @classmethod
    def get_items(cls):
        return cls.objects.filter(is_active=True, category__is_active=True).order_by('category', 'name')


class Contact(models.Model):
    city = models.CharField(verbose_name='город', max_length=64)
    phone = models.CharField(verbose_name='телефон', max_length=20)
    email = models.EmailField(verbose_name='email', max_length=254)
    is_active = models.BooleanField(verbose_name='активный', db_index=True, default=1)

    def __str__(self):
        return self.city
