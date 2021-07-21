from django.db import models
from django.db.models.deletion import CASCADE
from django.forms.widgets import Textarea


class ProdBrand(models.Model):
    brand = models.CharField(max_length=255)

    def __str__(self):
        return self.brand

class Products(models.Model):
    prod_name = models.CharField(max_length=255)
    prod_brand = models.ForeignKey(ProdBrand, on_delete=CASCADE)
    prod_images = models.ImageField()
    prod_description = models.TextField(default=None)
    prod_price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)