from django.contrib import admin
from .models import Address, Plans, UserDetails

admin.site.register(Address)
admin.site.register(Plans)
admin.site.register(UserDetails)
