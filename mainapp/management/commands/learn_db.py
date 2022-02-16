from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q, When, F, IntegerField, Case, DecimalField, Value, TextField
from prettytable import PrettyTable

from basketapp.views import print_queries
from mainapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):

        # вывести цены со скидкой для товаров из категории 1 или 2 или меньше 1000 - 10%, для товаров >= 1000 - 30%

        low_price_condition = Q(category_id=1) | Q(category_id=2) | Q(price__lt=1000)
        high_price_condition = Q(price__gte=1000)

        low_price_case = When(low_price_condition, then=Value('low'))
        high_price_case = When(high_price_condition, then=Value('high'))

        low_price = When(low_price_condition, then=F('price') * (1 - 10 / 100))
        high_price = When(high_price_condition, then=F('price') * (1 - 30 / 100))

        filter_products = Product.objects.annotate(
            price_case=Case(low_price_case, high_price_case, output_field=TextField())
        ).annotate(
            discount_price=Case(low_price, high_price, output_field=DecimalField())
        ).order_by('category_id', 'name').select_related('category')

        print(print_queries('SELECT', connection.queries))

        t_list = PrettyTable(["Категория", "Товар", "Акция", 'Цена', 'Цена со скидкой'])
        t_list.align = 'l'
        i = 0
        for product in filter_products:
            t_list.add_row([f'{product.category.name:15}', f'{product.name:15}', f'{product.price_case:5}',
                            f'{product.price:6.0f}',
                            f'{product.discount_price:6.0f}'])
            if i == 0:
                print(print_queries('SELECT', connection.queries))
                i += 1

        print(t_list)
