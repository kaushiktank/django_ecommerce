from django.urls import path
from .views import first_brands, home_page, shop_page, shop_brand

urlpatterns = [
    path('', home_page, name='homepage'),
    path('shop/', shop_page, name='shoppage'),
    path('shop/brand/', first_brands, name='all_brands'),
    path('shop/brand/', shop_brand, name='filter_by_brand'),
]
