from django.contrib import admin
from .models import Product
from .models import Cart
from .models import Token

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Token)
# Register your models here.
