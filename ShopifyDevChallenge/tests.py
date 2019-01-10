from django.test import TestCase
from .models import Product
from .models import Cart


class ProductTest(TestCase):

    @staticmethod
    def create_product(id="test_id", name="Test Product Name", price=100.0,count=10):
        return Product.objects.create(id=id,title=name,price=price,inventory_count=count)

    def test_product_creation(self):
        id = "sample_id"
        name = "Nice Product Name"
        price = 0.99
        count = 1000
        product = self.create_product(id, name, price, count)
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.id,id)
        self.assertEqual(product.title,name)
        self.assertEqual(product.price,price)
        self.assertEqual(product.inventory_count,count)