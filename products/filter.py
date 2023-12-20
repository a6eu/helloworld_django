import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'brand__name': ['iexact'],
            'category__name': ['iexact'],
        }


