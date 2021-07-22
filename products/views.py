from typing import get_type_hints
from django.shortcuts import render
from .models import Products, ProductCategory, ProductSubCategory, ProdBrand
# from .forms import FilterByBrandAndPrice


def get_brands_count():
    brands = ProdBrand.objects.all()
    brand_product = []
    for brand in brands:
        d = {}
        product_count = Products.objects.filter(prod_brand_id=brand.id).count()
        d['product_count'] = product_count
        d['brand_id'] = brand.id
        d['brand_name'] = brand.brand
        brand_product.append(d)

    return brand_product

def home_page(request):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'index.html', context)


def shop_page(request):
    category = ProductCategory.objects.all()
    subcategory = ProductSubCategory.objects.all()
    products = Products.objects.all()

    context = {'category': category,
               'subcategory': subcategory, 
               'products': products, 
               'brand_product': get_brands_count()}
    return render(request, 'shop.html', context)


def first_brands(request):
    brand_product = get_brands_count()
    products = Products.objects.filter(prod_brand=brand_product[0]['brand_id'])
    brand_name = brand_product[0]['brand_name']
    context = {'brand_product':brand_product,'products':products, 'brand_name':brand_name}
    return render(request, 'shop_brand.html', context)


def shop_brand(request):
    context = {'brand_product':get_brands_count()}

    return render(request, 'shop_brand.html', context)