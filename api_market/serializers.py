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

    def get_image_url(self, instance):
        if instance.image:
            return instance.image.url
        return None


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

    def get_image_url(self, instance):
        if instance.image:
            return instance.image.url
        return None



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

    def get_image_url(self, instance):
        if instance.image:
            return instance.image.url
        return None


class ProductLisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CommentWriteSerializer(serializers.ModelSerializer):
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


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'updated_at', 'user', "product"]
        read_only_fields = ['updated_at', 'user', "product", ]

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.updated_at = validated_data.get('updated_at', timezone.now())
        instance.save()
        return instance


class CommentListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    created_by = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'first_name', 'last_name', 'created_by', "rating", "content", "created_at", "updated_at"]
        read_only_fields = ['user']


class ProductsInBasketSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductsInBasket
        fields = ["id", 'product', "quantity", "total_price"]

    def get_total_price(self, product_item: ProductsInBasket):
        return product_item.quantity*product_item.product.price


class BasketSerializer(serializers.ModelSerializer):
    products = ProductsInBasketSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ['id', 'products', "total_price"]

    def get_total_price(self, product):
        return sum([product.quantity * product.product.price for product in product.products.all()])


class AddProductsInBasketSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Продукт с данным ключем отсутсвует')
        return value

    def validate_quantity(self, value):
        product_id = self.initial_data.get('product_id')
        product = Product.objects.get(pk=product_id)
        if value > product.quantity:
            raise serializers.ValidationError('Запрошенное количество превышает доступное количество продукта.')
        return value

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        basket_id = self.context['basket_id']
        product = Product.objects.get(pk=product_id)
        try:
            basket_product = ProductsInBasket.objects.get(basket_id=basket_id, product_id=product_id)
            basket_product.quantity += quantity
            basket_product.save()
            product.quantity -= quantity
            product.save()
            self.instance = basket_product
        except ProductsInBasket.DoesNotExist:
            self.instance = ProductsInBasket.objects.create(basket_id=basket_id, **self.validated_data)
            product.quantity -= quantity
            product.save()

    class Meta:
        model = ProductsInBasket
        fields = ['id', 'product_id', 'quantity']


