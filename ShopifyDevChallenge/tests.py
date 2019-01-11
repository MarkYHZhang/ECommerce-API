from django.test import TestCase
from .models import Product
from .models import Cart


class ProductTest(TestCase):

    @staticmethod
    def create_product(id="test_id", name="Test Product Name", price=100.0,count=10):
        return Product.objects.create(id=id,title=name,price=price,inventory_count=count)

    @staticmethod
    def create_cart(id="test_id", items=None, item_quantities=None, cost = 0):
        if item_quantities is None:
            item_quantities = []
        if items is None:
            items = []
        return Cart.objects.create(id=id,items=items,item_quantities=item_quantities, cost=cost)

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

    def test_cart_creation(self):
        id="test_Cart_id"
        items = ["product1","product2"]
        item_quantities = [10,20]
        cost=100
        cart = self.create_cart(id,items,item_quantities,cost)
        self.assertTrue(isinstance(cart, Cart))
        self.assertEqual(id,cart.id)
        self.assertEqual(items,cart.item)
        self.assertEqual(item_quantities,cart.item_quantities)
        self.assertEqual(cost,cart.cost)
