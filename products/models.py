from django.db import models
from django.db.models.deletion import CASCADE



class ProductCategory(models.Model):
    main_category = models.CharField(max_length=255)

    def __str__(self):
        return self.main_category


class ProductSubCategory(models.Model):
    sub_category = models.CharField(max_length=255)
    main_category_id = models.ForeignKey(ProductCategory, on_delete=CASCADE)

    def __str__(self):
        return self.sub_category


class ProdBrand(models.Model):
    brand = models.CharField(max_length=255)

    def __str__(self):
        return self.brand


class Products(models.Model):
    prod_name = models.CharField(max_length=255)
    prod_brand = models.ForeignKey(ProdBrand, on_delete=CASCADE)
    prod_images = models.ImageField(default=None, upload_to='images/')
    prod_description = models.TextField(default=None)
    prod_category = models.ForeignKey(ProductCategory, on_delete=CASCADE)
    prod_sub_category = models.ForeignKey(ProductSubCategory, on_delete=CASCADE)
    prod_price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.prod_name


class Cart(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    cart_quantity = models.IntegerField(default=1)

