from django.test import TestCase
from mainapp.models import ProductCategory, Product
from django.test.client import Client


class TestMainSmokeTest(TestCase):

    def setUp(self) -> None:
        category = ProductCategory.objects.create(name='Test', is_active=True)
        Product.objects.create(category=category, name='product_1', price=100, is_active=True)

        self.client = Client()

    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_category(self):
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category_{category.pk}/')
            self.assertEqual(response.status_code, 200)

    def test_product(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/{product_item.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        pass
