from django.urls import path
from .views import login_page, logout_page, register_page

urlpatterns = [
    path('login/', login_page, name='login_user'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
]
