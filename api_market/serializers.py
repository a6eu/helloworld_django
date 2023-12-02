from django.utils import timezone

from rest_framework import serializers
from rest_framework.response import *
from .models import *


class FilterReviewSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializers = self.parent.parent.__class__(value, context=self.context)
        return serializers.data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewSerializer
        model = Category
        fields = ("id", "name", "children")


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductSearchCreateSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = '__all__'


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


class ProductLisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['content', 'rating', 'created_at', 'updated_at', 'user', "product",]
        read_only_fields = ['updated_at', 'created_at', 'user', "product",]

    def create(self, validated_data):
        product_id = self.context['view'].kwargs.get('product_id')
        product_db = Product.objects.get(pk=product_id)
        validated_data['product'] = product_db
        return super().create(validated_data)


class CommentListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    created_by = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'first_name', 'last_name', 'created_by', "rating", "content", "created_at" ]
        read_only_fields = ['user']


