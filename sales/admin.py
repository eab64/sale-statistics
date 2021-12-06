from django.contrib import admin

from .models import Seller, Product, Sale

admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Sale)