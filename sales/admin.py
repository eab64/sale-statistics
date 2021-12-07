from django.contrib import admin

from .models import Seller, Product, Sale, WeekPlan

admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(WeekPlan)