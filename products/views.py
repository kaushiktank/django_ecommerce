from django.http.response import JsonResponse
from products.forms import CartForm, SearchForm
from typing import get_type_hints
from django.shortcuts import redirect, render
from .models import Cart, Products, ProductCategory, ProductSubCategory, ProdBrand
from django.contrib.auth.decorators import login_required
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


def get_category_count():
    category = ProductCategory.objects.all()
    product_category = []
    for cat in category:
        d = {}
        category_count = Products.objects.filter(prod_category_id=cat.id).count()
        d['category_count'] = category_count
        d['category_id'] = cat.id
        d['category_name'] = cat.main_category
        product_category.append(d)

    return product_category

def home_page(request):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'index.html', context)


def shop_page(request):
    category = get_category_count()
    subcategory = ProductSubCategory.objects.all()
    products = Products.objects.all()

    context = {'category': category,
               'subcategory': subcategory, 
               'products': products, 
               'brand_product': get_brands_count(),
               'browse_categoty': get_category_count()}
    return render(request, 'shop.html', context)


def first_brands(request):
    brand_product = get_brands_count()
    products = Products.objects.filter(prod_brand=brand_product[0]['brand_id'])
    brand_name = brand_product[0]['brand_name']
    context = {'brand_product':brand_product,'products':products, 'brand_name':brand_name}
    return render(request, 'shop_brand.html', context)


def shop_brand(request, brand_id):
    products = Products.objects.filter(prod_brand_id = brand_id)
    if len(products) >= 1:
        context = {'brand_product':get_brands_count(), 'products':products}
    else:
        context = {'brand_product':get_brands_count(), 'custom_message':"No Data Found"}
    return render(request, 'shop_brand.html', context)


def product_details(request, product_id):
    print("product category")
    product_details = Products.objects.filter(id = product_id)
    product_category = ProductCategory.objects.filter(id = product_details[0].prod_category_id)[0]
    context = {'product_details':product_details, 'product_category':product_category}
    return render(request, 'single_product.html', context)


@login_required(login_url='users:login_user')
def add_to_cart(request):
    if request.method =="POST":
        form = CartForm(request.POST)
        print("form is assigned")
        if form.is_valid():
            print("for is valid")
            user_id = request.POST['user_id']
            product_id = request.POST['product_id']
            cart_quantity = request.POST['cart_quantity']
            cart_obj = Cart(user_id = user_id, product_id = product_id, cart_quantity = cart_quantity)
            cart_obj.save()
            return JsonResponse({'status':'save'})
        else:
            return JsonResponse({'status':0})


def get_search_results(request):
    form = SearchForm(request.GET)
    print(form)
    search = Products.objects.filter(prod_name__contains = 'google')
    context = {'products':search}
    return render(request, 'search_result.html', context)


def first_category(request):
    category = get_category_count()
    category_name = category[0]['category_name']
    products = Products.objects.filter(prod_category_id=category[0]['category_id'])
    context = {'categorys':category, 'category_name':category_name,'products':products}
    return render(request, 'shop_category.html', context)


def filter_category(request, category_id):
    products = Products.objects.filter(prod_category_id = category_id)
    if len(products) >= 1:
        context = {'categorys':get_category_count(), 'products':products}
    else:
        context = {'categorys':get_category_count(), 'custom_message':"No Data Found"}

    return render(request, 'shop_category.html', context)


def get_cart_details(request):
    cart = Cart.objects.filter(user_id = request.user.id)
    cart_product = []
    for id in cart:
        cart_product.append(Products.objects.filter(id = id.product_id)[0])
    
    cart_price = []
    for x in range(len(cart)):
        d = {}
        d['total_price'] = (cart_product[x].prod_price) * (cart[x].cart_quantity)
        d['cart_quantity'] = cart[x].cart_quantity
        d['cart_id'] = cart_product[x].id
        print(d)
        cart_price.append(d)

    sub_total = 0
    gst = 0
    for n in cart_price:
        sub_total = sub_total + n['total_price']
        gst = gst + ( 0.18 * n['total_price'])

    grand_total = gst + sub_total
    context = {'cart_product':cart_product, 'cart':cart, 'cart_price':cart_price, 'grand_total':grand_total,'gst':gst, 'sub_total':sub_total}
    return render(request, 'cart.html', context)