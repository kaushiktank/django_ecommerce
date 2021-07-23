from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.address_line_1 +", "+ self.address_line_2


class UserMobileNo(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    mobile_number = models.CharField(max_length=15)
    alternative_mobile_number = models.CharField(max_length=15) 

    def __str__(self):
        return self.mobile_number