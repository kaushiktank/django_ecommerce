from django.contrib import admin
from .models import *

admin.site.register(Address)
admin.site.register(Plans)
admin.site.register(UserDetails)
admin.site.register(UserPlans)