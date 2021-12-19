from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product, Contact
import json
import os

JSON_PATH = 'mainapp/json'


def load_to_json(file_name, data):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'w') as f:
        return f.write(json.dumps(data))


class Command(BaseCommand):
    def handle(self, *args, **options):

        categories = []
        for category in ProductCategory.objects.all():
            categories.append({
                'name': category.name,
                'description': category.description,
                'is_active': category.is_active
            })

        load_to_json('categories', categories)

        products = []
        for product in Product.objects.all():
            products.append({
                'category': product.category.name,
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'quantity': product.quantity,
                'image': str(product.image),
                'is_active': product.is_active
            })

        load_to_json('products', products)

        contacts = []
        for contact in Contact.objects.all():
            contacts.append({
                'city': contact.city,
                'phone': contact.phone,
                'email': contact.email,
                'is_active': contact.is_active
            })

        load_to_json('contacts', contacts)


