from .models import Product
from django.http import HttpResponse
from .models import Cart
from django.core.serializers import serialize
from ratelimit.decorators import ratelimit
from. responsegenerator import invalid
from. responsegenerator import missing
from. responsegenerator import empty
import uuid

#rate limit by ip for maximum of 1 request per 5 seconds
@ratelimit(key='ip', rate='1/5s')
def retrieve(request):
    if request.POST:
        products = Product.objects.all()
        available_inventory_only = False
        if "availableInventoryOnly" in request.POST and request.POST["availableInventoryOnly"] == "true":
            available_inventory_only = True
        if "products" in request.POST:
            product_ids = request.POST["products"]
            for product_id in product_ids:
                if available_inventory_only:
                    products = products.filter(id=product_id, inventory_count__gt=0)
                else:
                    products = products.filter(id=product_id)
        elif "all" in request.POST:
            if available_inventory_only:
                products = products.filter(inventory_count__gt=0)
        return HttpResponse(serialize('json', products))


#rate limit by ip for maximum of 1 request per 45 seconds
@ratelimit(key='ip', rate='1/1m')
def create_cart(request):
    if request.GET:
        cart_id = str(uuid.uuid4())
        Cart.objects.create(uuid=cart_id)
        return HttpResponse(cart_id)


valid_actions = ["add", "remove"]

def modify_cart(request):
    if request.POST:

        if "cart_id" not in request.POST:
            return missing("cart id")
        if "items" not in request.POST:
            return missing("items array")

        if not Cart.objects.filter(id=request.POST['cart_id']).exists():
            return invalid("cart id")
        if request.POST['items'] == "":
            return empty("items array")

        action = request.POST['type']
        cart_id = request.POST['cart_id']
        items = request.POST['items']

        for item in items:
            if "action" not in item:
                return missing("action type")
            if "action" not in valid_actions:
                return invalid("action")

            if "product_id" not in item:
                return missing("product ID")
            product_id = item["product_id"]
            if not Product.objects.filter(id=product_id).exists():
                return invalid("product ID")

            if "quantity" not in item:
                return missing("quantity")
            if item["quantity"] <= 0 and not isinstance(item["quantity"], int):
                return invalid("quantity")
