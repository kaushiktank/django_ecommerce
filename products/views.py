from typing import List
from django.http import request
from products.tasks import send_order_email_task
from django.contrib.auth import models
from django.forms.utils import pretty_name
from users.models import Address
from django.http.response import JsonResponse
from products.forms import CartForm, OrdersForm
from django.shortcuts import redirect, render
from .models import Cart, Products, ProductCategory, ProductSubCategory, ProdBrand
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView


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
    products = Products.objects.all()[:20]
    context = {'products': products}
    return render(request, 'index.html', context)


def shop_page(request):
    category = get_category_count()
    subcategory = ProductSubCategory.objects.all()
    products = Products.objects.all()[:20]

    context = {'category': category,
               'subcategory': subcategory, 
               'products': products, 
               'brand_product': get_brands_count(),
               'browse_categoty': get_category_count()}
    return render(request, 'shop.html', context)


# def first_brands(request):
#     brand_product = get_brands_count()
#     products = Products.objects.filter(prod_brand=brand_product[0]['brand_id'])[:20]
#     brand_name = brand_product[0]['brand_name']
#     context = {'brand_product':brand_product,'products':products, 'brand_name':brand_name}
#     return render(request, 'shop_brand.html', context)

class FirstBrand(ListView):
    model = ProdBrand
    template_name = 'shop_brand.html'
    context_object_name = 'brand_product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_brand = ProdBrand.objects.all()
        # print(product_brand)
        context["products"] = Products.objects.filter(prod_brand=product_brand[0].id)[:20]
        context['brand_name'] = product_brand[0].brand
        # print(context)
        return context
    

class ShopBrand(ListView):
    model = ProdBrand
    template_name = 'shop_brand.html'
    context_object_name = 'brand_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print("Brand ID: ",self.kwargs.brand_id)
        prod = Products.objects.filter(prod_brand_id = self.kwargs.brand_id)
        if len(prod) >= 1:
            context["products"] = prod
        else:
            context['custom_message'] = "No Data Found"

        return context


# def shop_brand(request, brand_id):
#     products = Products.objects.filter(prod_brand_id = brand_id)[:20]
#     if len(products) >= 1:
#         context = {'brand_product':get_brands_count(), 'products':products}
#     else:
#         context = {'brand_product':get_brands_count(), 'custom_message':"No Data Found"}
#     return render(request, 'shop_brand.html', context)


def product_details(request, product_id):
    # print("product category")
    product_details = Products.objects.filter(id = product_id)
    product_category = ProductCategory.objects.filter(id = product_details[0].prod_category_id)[0]
    context = {'product_details':product_details, 'product_category':product_category}
    return render(request, 'single_product.html', context)


@login_required(login_url='users:login_user')
def add_to_cart(request):
    if request.method =="POST":
        form = CartForm(request.POST)
        if form.is_valid():
            # print("for is valid")
            form.save()
            return JsonResponse({'status':'save'})
        else:
            return JsonResponse({'status':0})



class GetSearchResult(ListView):
    queryset = ProductCategory.objects.all()
    template_name = 'search_result.html'
    context = {}
    context['product_category'] = queryset
    context['custom_messages'] = "Make your Search"

    def post(self, request, *args, **kwargs):
        search_query = request.POST['search']
        # print('post methoad is identfyed')
        try:
            if request.POST['dropdown']:
                category_id = request.POST['dropdown']
                self.context["products"] = Products.objects.filter(prod_category_id = category_id ,prod_name__contains = search_query)[:20]
        except:
            self.context['products'] = Products.objects.filter(prod_name__contains = search_query)[:20]
        
        if len(self.context['products']) == 0:
            self.context['custom_messages'] = 'No Data Found'

        return render(request, 'search_result.html', self.context)

        
    
    # queryset = ProductCategory.objects.all()
    # context_object_name = 'product_category'
    # if request.method == 'POST':
    #     context['products'] = ""




def first_category(request):
    category = get_category_count()
    category_name = category[0]['category_name']
    products = Products.objects.filter(prod_category_id=category[0]['category_id'])[:20]
    context = {'categorys':category, 'category_name':category_name,'products':products}
    return render(request, 'shop_category.html', context)


def filter_category(request, category_id):
    products = Products.objects.filter(prod_category_id = category_id)[:20]
    if len(products) >= 1:
        context = {'categorys':get_category_count(), 'products':products}
    else:
        context = {'categorys':get_category_count(), 'custom_message':"No Data Found"}

    return render(request, 'shop_category.html', context)


def get_cart_details(request):

    cart = Cart.objects.filter(user_id = request.user.id)
    address = Address.objects.filter(user_id = request.user.id)[0]
    cart_product = []
    for id in cart:
        cart_product.append(Products.objects.filter(id = id.product_id)[0])
    
    cart_price = []
    for x in range(len(cart)):
        d = {}
        d['total_price'] = (cart_product[x].prod_price) * (cart[x].cart_quantity)
        d['cart_quantity'] = cart[x].cart_quantity
        d['cart_id'] = cart_product[x].id
        cart_price.append(d)

    sub_total = 0
    gst = 0
    for n in cart_price:
        sub_total = sub_total + n['total_price']
        gst = gst + ( 0.18 * n['total_price'])

    grand_total = gst + sub_total
    context = {'cart_product':cart_product, 'cart':cart, 'cart_price':cart_price, 'grand_total':grand_total,'gst':gst, 'sub_total':sub_total, 'address':address}
    return render(request, 'cart.html', context)


def confirmation(request):
    cart = Cart.objects.filter(user_id = request.user.id)[0]
    # print('cart is assigned')
    def sent_email():
        # print("sent function is called")
        name = request.user.username
        email = request.user.email
        product = Products.objects.filter(id = cart.product_id)[0]
        order = product.prod_name
        if product.quantity >= cart.cart_quantity:
            email_file = 'email_message_avaliable.html'
        else:
            email_file = 'email_message.html'
        send_order_email_task.delay(name, email, order, email_file)

    sent_email()

    # if request.method == 'POST':
    #     form = OrdersForm(request.POST)
    #     print('form is assigned')
    #     print(form)
    #     user_id = request.POST.get('user_id')
    #     product_id = request.POST.get('product_id')
    #     quantity = request.POST.get('quantity')
    #     address = request.POST.get('address')
    #     mobile = request.POST.get('mobile')
    #     print('user_id: ' +user_id+ ' product_id: ' +product_id+ ' quantity: ' +quantity+ ' address: '+address+' mobile: '+mobile)
        # form.save()

        # if form.is_valid():
        #     print('form is validetes')
        #     form.save()

            # sent an email here
            # delete recoard in cart
        # cart = Cart.objects.filter(user_id = request.user.id)
        # cart.delete()

    return render (request, 'confirmation.html')