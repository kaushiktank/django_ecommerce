from django.contrib import admin
from django.urls import path
from users import views as userView
from products import views as prodView


urlpatterns = [
    path('',prodView.home_page, name='homepage'),
    path('admin/', admin.site.urls),
    path('login/', userView.login_page, name='login_user'),
    path('logout/', userView.logout_page, name='logout'),
    path('register/', userView.register_page, name='register'),
]
