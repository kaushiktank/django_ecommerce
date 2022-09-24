from users.models import Address
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    main_category = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Category"
        
    def __str__(self):
        return self.main_category


class ProductSubCategory(models.Model):
    sub_category = models.CharField(max_length=255)
    main_category_id = models.ForeignKey(ProductCategory, on_delete=CASCADE)

    class Meta:
        verbose_name_plural = "Sub Category"

    def __str__(self):
        return self.sub_category


class ProdBrand(models.Model):
    brand = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Brands"

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

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.prod_name
    


class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    product_id = models.IntegerField()
    cart_quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "User Cart"


class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    total_amount = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=CASCADE)
    order_date_time = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=150, null=True)
    order_note = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "User Orders"

    def __str__(self):
        return str(self.id)


class OrderItems(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    order_id = models.ForeignKey(Orders, on_delete=CASCADE)
    item_id = models.ForeignKey(Products, on_delete=CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        verbose_name_plural = "User Order Items"

    def __str__(self):
        return str(self.id)