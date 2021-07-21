from django.contrib import admin
from django.urls import path
from users import views as userView
from products import views as prodView


urlpatterns = [
    path('',prodView.home_page),
    path('admin/', admin.site.urls),
]
