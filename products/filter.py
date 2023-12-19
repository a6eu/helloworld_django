import django_filters
from django.db.models import Q
from .models import Product


class ProductFilter(django_filters.FilterSet):
    category_name_and_parent_name = django_filters.CharFilter(method='filter_category_name_and_parent_name', label='Category Name or Parent Name')

    class Meta:
        model = Product
        fields = {
            'brand__name': ['iexact'],
        }

    def filter_category_name_and_parent_name(self, queryset, name, value):
        return queryset.filter(
            Q(category__name__iexact=value) | Q(category__parent__name__iexact=value)
        )
