from django.contrib import admin

from .models import Basket, Order, Purchase

admin.site.register(Order)
admin.site.register(Purchase)
admin.site.register(Basket)
