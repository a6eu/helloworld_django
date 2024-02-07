from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category
from django import forms
# Register your models here.


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].label = 'categoryId'


class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    form = CategoryForm
    list_display = ('name', 'categoryId')


admin.site.register(Category, CustomMPTTModelAdmin)

