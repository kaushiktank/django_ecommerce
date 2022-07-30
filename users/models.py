from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    address_line_1 = models.CharField(max_length=255, default=None)
    address_line_2 = models.CharField(max_length=255, default=None)
    city = models.CharField(max_length=255, default=None)
    state = models.CharField(max_length=255, default=None)
    zip_code = models.CharField(max_length=20, default=None)
    country = models.CharField(max_length=255, default=None)
    mobile_number = models.CharField(max_length=15, default=None)
    alternative_mobile_number = models.CharField(max_length=15, default=None) 

    def __str__(self):
        return self.address_line_1 +", "+ self.address_line_2

class Plans(models.Model):
    title = models.CharField(max_length=255, default=None)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.title


class UserDetails(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    user_name = models.CharField(max_length=255, default=None, null=True, blank=True)
    plan = models.ForeignKey(Plans, on_delete=CASCADE, default=None, null=True, )
    verification = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, default=None)

