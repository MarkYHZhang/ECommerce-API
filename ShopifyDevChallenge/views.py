from .models import Product
from .models import Token
from django.http import HttpResponse
from .models import Cart
from django.core.serializers import serialize
from ratelimit.decorators import ratelimit
from .responsegenerator import invalid
from .responsegenerator import missing
from .responsegenerator import access_denied
from .responsegenerator import empty
from .responsegenerator import response
from .responsegenerator import response_no_format
import uuid
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import Serializer
from secrets import token_hex
from time import time


max_token_expiry_interval = 60 # 3 hours


def raw_jsonify(string, id_name):
    return string.replace("\\\"","\"").replace("\"[","[").replace("]\"","]").replace("\"pk\"","\""+id_name+"\"")


def jsonify(obj, id_name, cnt):
    return HttpResponse(raw_jsonify(CustomSerializer().serialize(obj),id_name))


class CustomSerializer(Serializer):
    def get_dump_object(self, obj):
        dump_object = self._current or {}
        dump_object.update({'pk': (obj._get_pk_val())})
        return dump_object


@csrf_exempt
@ratelimit(key='ip', rate='1/60s')
def access_token(request):
    token = token_hex(24)
    timestp = int(time())
    Token.objects.create(token=token,timestamp=timestp)
    return response_no_format(token)

# rate limit by ip for maximum of 1 request per 5 seconds
@csrf_exempt
@ratelimit(key='ip', rate='1/5s')
def retrieve_products(request):

    token = request.GET.get('token', '')
    if not Token.objects.filter(token=token).exists() or int(time())-Token.objects.get(token=token).timestamp > max_token_expiry_interval:
        Token.objects.filter(token=token).delete()
        return access_denied()

    if request.body:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        products = Product.objects.all()
        available_inventory_only = False
        if "availableInventoryOnly" in body and body["availableInventoryOnly"] == "true":
            available_inventory_only = True
        if "products" in body:
            product_ids = body["products"]
            products = Product.objects.filter(id__in=product_ids)
            if available_inventory_only:
                products = Product.objects.filter(inventory_count__gt=0)
        elif "all" in body:
            if available_inventory_only:
                products = products.filter(inventory_count__gt=0)
        return HttpResponse(jsonify(products,"product_id",1000))
    return HttpResponse("API ACCESS ONLY")

@csrf_exempt
# rate limit by ip for maximum of 1 request per 45 seconds
@ratelimit(key='ip', rate='1/1m')
def create_cart(request):
    token = request.GET.get('token', '')
    if not Token.objects.filter(token=token).exists() or int(time())-Token.objects.get(token=token).timestamp > max_token_expiry_interval:
        Token.objects.filter(token=token).delete()
        return access_denied()

    cart_id = uuid.uuid4()
    print(cart_id)
    Cart.objects.create(id=cart_id)
    return response_no_format(str(cart_id))

@csrf_exempt
def discard_cart(request):
    token = request.GET.get('token', '')
    if not Token.objects.filter(token=token).exists() or int(time())-Token.objects.get(token=token).timestamp > max_token_expiry_interval:
        Token.objects.filter(token=token).delete()
        return access_denied()

    if request.body:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if "cart_id" not in body:
            return missing("cart id")
        if not Cart.objects.filter(id=body['cart_id']).exists():
            return invalid("cart id")
        Cart.objects.filter(id=body['cart_id']).delete()
        return response("removed")
    return HttpResponse("API ACCESS ONLY")


@csrf_exempt
def checkout_cart(request):
    token = request.GET.get('token', '')
    if not Token.objects.filter(token=token).exists() or int(time())-Token.objects.get(token=token).timestamp > max_token_expiry_interval:
        Token.objects.filter(token=token).delete()
        return access_denied()

    if request.body:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if "cart_id" not in body:
            return missing("cart id")
        if not Cart.objects.filter(id=body['cart_id']).exists():
            return invalid("cart id")

        cart_id = body['cart_id']
        cartobj = Cart.objects.filter(id=cart_id)
        cart = Cart.objects.get(id=cart_id)
        for index, item in enumerate(cart.items):
            print(index, item)
            cur_product = Product.objects.get(id=item)
            quantity = cart.item_quantities[index]

            if cur_product.inventory_count - quantity < 0:
                return response("lack inventory for (" + item[0]+")")

            cur_product.inventory_count -= quantity
            cur_product.save()
        result = jsonify(cartobj, "cart_id", len(cartobj[0].items))
        Cart.objects.filter(id=cart_id).delete()
        return result
    return HttpResponse("API ACCESS ONLY")


valid_actions = ["add", "remove"]


@csrf_exempt
def modify_cart(request):
    token = request.GET.get('token', '')
    if not Token.objects.filter(token=token).exists() or int(time())-Token.objects.get(token=token).timestamp > max_token_expiry_interval:
        Token.objects.filter(token=token).delete()
        return access_denied()

    if request.body:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if "cart_id" not in body:
            return missing("cart id")
        if "items" not in body:
            return missing("items array")

        if not Cart.objects.filter(id=body['cart_id']).exists():
            return invalid("cart id")
        if body['items'] == "":
            return empty("items array")

        cart_id = body['cart_id']
        cartobj = Cart.objects.filter(id=cart_id)
        cart = Cart.objects.get(id=cart_id)
        items = body['items']

        for item in items:
            if "action" not in item:
                return missing("action type")
            if item["action"] not in valid_actions:
                return invalid("action")

            if "product_id" not in item:
                return missing("product ID")
            product_id = item["product_id"]
            if not Product.objects.filter(id=product_id).exists():
                return invalid("product ID")

            if "quantity" not in item:
                return missing("quantity")
            if not isinstance(item["quantity"], int) or int(item["quantity"]) <= 0:
                return invalid("quantity")

            quantity = int(item["quantity"])
            cur_product = Product.objects.get(id=product_id)

            if item["action"] == "add":
                if cur_product.id in cart.items:
                    ind = cart.items.index(cur_product.id)
                    cart.item_quantities[ind] += quantity
                else:
                    cart.items.append(cur_product.id)
                    cart.item_quantities.append(quantity)
                cart.cost += quantity*cur_product.price
            else:
                if cur_product.id not in cart.items:
                    return invalid("product")
                ind = cart.items.index(cur_product.id)
                cart.item_quantities[ind] -= min(cart.item_quantities[ind],quantity)
                if cart.item_quantities[ind] <= 0:
                    del cart.items[ind]
                    del cart.item_quantities[ind]
                cart.cost -= quantity*cur_product.price
            cart.save()
        return jsonify(cartobj, "cart_id", len(cartobj[0].items))
    return HttpResponse("API ACCESS ONLY")

