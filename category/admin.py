from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category
# Register your models here.


class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20


admin.site.register(Category, CustomMPTTModelAdmin)

