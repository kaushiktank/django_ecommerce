from django.contrib import admin
from .models import Cart, ProdBrand, ProductCategory, ProductSubCategory, Products

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('prod_name','prod_brand','prod_price','quantity')


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('main_category')


class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category')

admin.site.register(ProdBrand)
admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(Cart)