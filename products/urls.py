from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import FirstBrand, GetSearchResult, ShopBrand, add_to_cart, confirmation, filter_category, first_category, get_cart_details, home_page, product_details, shop_page

urlpatterns = [
    path('', home_page, name='homepage'),
    path('shop/', shop_page, name='shoppage'),
    path('cart/', get_cart_details, name='get_cart_details'),
    path('shop/brand/', FirstBrand.as_view(), name='all_brands'),
    path('shop/brand/<int:brand_id>/', ShopBrand, name='filter_by_brand'),
    path('shop/category/', first_category, name='all_category'),
    path('shop/category/<int:category_id>/', filter_category, name='filter_by_category'),
    path('shop/product/<int:product_id>/', product_details, name='product_details'),
    path('addcart/', add_to_cart, name='add_to_cart'),
    path('search/', GetSearchResult.as_view(), name='get_search_results'),
    path('confirmation/', confirmation, name='confirmation')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
