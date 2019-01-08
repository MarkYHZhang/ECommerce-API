from django.db import models
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100, null=True)
    price = models.DecimalField()
    inventory_count = models.IntegerField()


class Cart(models.Model):
    id = models.UUIDField(primary_key=True)
    items = ArrayField(Product, models.IntegerField())