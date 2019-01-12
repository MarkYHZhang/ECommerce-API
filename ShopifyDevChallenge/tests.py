from django.test import TestCase
from django.test import Client
from .models import Product
from .models import Cart
from random import randint
from .views import jsonify


def create_product(id="test_id", name="Test Product Name", price=100.00, count=10):
    return Product.objects.create(id=id, title=name, price=price, inventory_count=count)


def create_cart(id="test_id", items=None, item_quantities=None, cost = 0):
    if item_quantities is None:
        item_quantities = []
    if items is None:
        items = []
    return Cart.objects.create(id=id,items=items,item_quantities=item_quantities, cost=cost)

#http://blog.appliedinformaticsinc.com/test-client-as-testing-tool-for-get-and-post-requests-in-django/
class RestfulTest(TestCase):

    @classmethod
    def setUpClass(self):
        # creating instance of a client.
        self.client = Client()

    def test_retrieve_product(self):
        random_id = "test_product_"+randint(100000000,999999999)
        create_product(id=random_id)

        list_with_filter_response = self.client.post('/retrieveProducts', {
          "availableInventoryOnly": "false",
          "products":[
              random_id,
          ]
        })
        self.assertEqual(list_with_filter_response.status_code, 302)
        test_against = jsonify(Product.objects.filter(id=random_id),"product_id")
        self.assertEqual(test_against, list_with_filter_response)

    def test_create_cart(self):
        response = self.client.get("/createCart")
        self.assertTrue(Cart.objects.filter(id=response).exists())

    def test_checkout_cart(self):
        random_cart_id = "test_cart_" + randint(100000000, 999999999)
        random_product_id = "test_product_"+randint(100000000,999999999)
        product = create_product(id=random_cart_id,count=1)
        response_invalid_id = self.client.post("/checkoutCart",{
          "cart_id": "some_invalid_id"
        })
        self.assertEqual(response_invalid_id,"INVALID_CART_ID")
        cart = create_cart(random_cart_id, [random_product_id],[10],10)
        response_lack_inventory = self.client.post("checkoutCart",{
            "cart_id": random_cart_id
        })
        self.assertEqual(response_lack_inventory,"LACK_INVENTORY_FOR_("+random_product_id.upper()+")")
        product.inventory_count = 100
        response_valid = self.client.post("checkoutCart",{
            "cart_id": random_cart_id
        })
        self.assertEqual(response_valid, "CHECKOUT SUCCESS")

    def test_discard_cart(self):
        random_cart_id = "test_cart_" + randint(100000000, 999999999)
        cart = create_cart(random_cart_id)
        response = self.client.post("discardCart",{
          "cart_id": "17215779-97ab-493a-9570-d909ebc48c73"
        })
        self.assertEqual(response,"REMOVED")



class DBTest(TestCase):

    def test_product_creation(self):
        id = "sample_id"
        name = "Nice Product Name"
        price = 0.99
        count = 1000
        product = create_product(id, name, price, count)
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
        cart = create_cart(id,items,item_quantities,cost)
        self.assertTrue(isinstance(cart, Cart))
        self.assertEqual(id,cart.id)
        self.assertEqual(items,cart.item)
        self.assertEqual(item_quantities,cart.item_quantities)
        self.assertEqual(cost,cart.cost)
