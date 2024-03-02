from rest_framework import serializers
from brand.models import Brand
from category.models import Category
from .models import Product
from brand.serializers import BrandSerializer, BrandIdNameSerializer
from category.serializers import CategoryNameIdSerializer


class ProductSearchCreateSerializer(serializers.ModelSerializer):
    brand = BrandIdNameSerializer(read_only=True)
    category = CategoryNameIdSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "price", "description", "brand", "category", "rating_total", "img_url", "quantity")


class ProductUpdateSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_image_url(self, instance):
        if instance.image:
            return instance.image.url
        return None


class ProductLisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductReadSerializer(serializers.ModelSerializer):
    brand_logo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'img_url', 'brand_logo_url', 'price']

    def get_brand_logo_url(self, instance):
        if instance.brand:
            return instance.brand.logo_url.url

