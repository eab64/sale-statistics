import datetime

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, timedelta


class Seller(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.first_name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    seller = models.ForeignKey(Seller, null = True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'sale date: {self.date_created}'


class WeekPlan(models.Model):
    seller = models.ForeignKey(Seller, null=True, on_delete=models.CASCADE)
    amount = models.FloatField(null=True)
    closing_time = models.DateTimeField(default=datetime.now()+timedelta(days=7))

    def __str__(self):
        return self.seller.first_name
