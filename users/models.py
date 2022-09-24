from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, default=None)
    address_line_2 = models.CharField(max_length=255, default=None)
    city = models.CharField(max_length=255, default=None)
    state = models.CharField(max_length=255, default=None)
    zip_code = models.CharField(max_length=20, default=None)
    country = models.CharField(max_length=255, default=None)
    mobile_number = models.CharField(max_length=15, default=None)
    alternative_mobile_number = models.CharField(max_length=15, default=None, blank=True, null=True) 

    def __str__(self):
        return self.address_line_1 +", "+ self.address_line_2

plan_durations = [(str(num), str(num) + " Months") for num in range(1, 13)]

class Plans(models.Model):
    title = models.CharField(max_length=255, default=None)
    price = models.FloatField(default=0)
    # This active is to identify the current running plans and older or expired plans which used to be active for certain time periods
    active = models.BooleanField(default=True)
    # is_default = Default plan for new users.
    is_default = models.BooleanField(default=False)
    durations = models.CharField(choices=plan_durations, max_length=50)

    def __str__(self):
        return self.title


class UserDetails(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    user_name = models.CharField(max_length=255, default=None, null=True, blank=True)
    verification = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, default=None)
    

class UserPlans(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    plan = models.ForeignKey(Plans, on_delete=CASCADE, default=None, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True, default=0)
    activated_date = models.DateTimeField(null=True, blank=True, default=None)
    expire_date = models.DateTimeField(null=True, blank=True, default=None)
    active = models.BooleanField(default=False)

    


