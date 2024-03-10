from django.db.models import Prefetch
from .models import Category


def prefetch_category_tree(queryset, levels):
    if levels <= 0:
        return queryset
    return queryset.prefetch_related(
        Prefetch('children', queryset=prefetch_category_tree(Category.objects.all(), levels-1))
    )