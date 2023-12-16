from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin

# Register your models here.
class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20


admin.site.register(Category, CustomMPTTModelAdmin)
admin.site.register(Product),
admin.site.register(Brand),
admin.site.register(Order),
admin.site.register(PaymentStatus),
admin.site.register(Basket),
admin.site.register(ProductsInBasket),
admin.site.register(Comment),
admin.site.register(Favorites),
admin.site.register(Reply),






