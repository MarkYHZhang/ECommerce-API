from django.db import models
from django.contrib.postgres.fields import ArrayField

class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    inventory_count = models.IntegerField()


class Cart(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    items = ArrayField(models.CharField(max_length=100), null=True, default=list)
    item_quantities = ArrayField(models.IntegerField(), null=True, default=list)
    cost = models.DecimalField(decimal_places=2, max_digits=8, default=0)


class Token(models.Model):
    token = models.CharField(max_length=65)
    timestamp = models.IntegerField()