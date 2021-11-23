from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя категории', max_length=64)
    description = models.TextField(verbose_name='описание категории', blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default=1)
    image = models.ImageField(upload_to='products_images', blank=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    @property
    def url(self):
        return reverse('mainapp:products:product', kwargs={'pk': self.id})


class Contact(models.Model):
    city = models.CharField(verbose_name='город', max_length=64)
    phone = models.CharField(verbose_name='телефон', max_length=20)
    email = models.CharField(verbose_name='email', max_length=64)

    def __str__(self):
        return self.city
