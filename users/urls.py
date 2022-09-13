from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_page, name='login_user'),
    path('plans/', plans, name='plans'),
    path('update_plan/', update_plan, name='update_plan'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/edit/', edit_user_profile, name='edit_user_profile'),
    path('verification/<str:token>/', verification, name='verification'),
    path('resend_verification/', resend_verification, name='resend_verification'),
    path('user_address/', user_address, name='user_address'),
    path('order_history/', order_history, name='order_history')
]
