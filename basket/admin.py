from django.contrib import admin
from .models import Basket, ProductsInBasket
# Register your models here.

admin.site.register(Basket),
admin.site.register(ProductsInBasket),