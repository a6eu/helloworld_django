import django_filters
from django.db.models import Q
from .models import Product
from category.models import Category

class ProductFilter(django_filters.FilterSet):
    category_id_or_parent_id = django_filters.CharFilter(method='filter_by_category_id_or_parent_id')

    class Meta:
        model = Product
        fields = {
            'brand__name': ['iexact'],
        }

    def filter_by_category_id_or_parent_id(self, queryset, name, value):
        category = Category.objects.filter(categoryId=value).first()
        if category:
            descendant_ids = category.get_descendants(include_self=True).values_list('id', flat=True)
            print(descendant_ids)
            queryset = queryset.filter(category__id__in=descendant_ids)
        return queryset


