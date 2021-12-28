from django.core.management.base import BaseCommand
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, Contact
import json
import os

JSON_PATH = 'mainapp/fixtures'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')
        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]
            # Получаем категорию по имени
            _category = ProductCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        contacts = load_from_json('contacts')
        Contact.objects.all().delete()
        for contact in contacts:
            new_contact = Contact(**contact)
            new_contact.save()

        if not ShopUser.objects.filter(username='django').exists():
            ShopUser.objects.create_superuser(username='django', email='django@geekshop.local', password='geekbrains')


