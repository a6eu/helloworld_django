from rest_framework import serializers
from products.serializers import ProductDetailSerializer
from .models import Favorites


class FavoritesSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)

    class Meta:
        model = Favorites
        fields = ['product']