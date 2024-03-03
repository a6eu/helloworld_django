from rest_framework import serializers
from products.serializers import ProductDetailSerializer
from products.models import Product
from .models import *


class ProductsInBasketSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductsInBasket
        fields = ["id", 'product', "quantity", "total_price"]

    def get_total_price(self, product_item: ProductsInBasket):
        return product_item.quantity * product_item.product.price


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

    def validate(self, data):
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not Product.objects.filter(pk=product_id).exists():
            raise serializers.ValidationError('Продукт с данным ключем отсутствует')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Продукт с данным ключем отсутствует')

        if quantity > product.quantity:
            raise serializers.ValidationError('Запрошенное количество превышает доступное количество продукта.')

        return data

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        basket_id = self.context['basket_id']
        try:
            basket_product = ProductsInBasket.objects.get(basket_id=basket_id, product_id=product_id)
            basket_product.quantity += quantity
            basket_product.save()
            self.instance = basket_product
        except ProductsInBasket.DoesNotExist:
            self.instance = ProductsInBasket.objects.create(basket_id=basket_id, **self.validated_data)

    class Meta:
        model = ProductsInBasket
        fields = ['id', 'product_id', 'quantity']


class DeleteOrPatchProduct(serializers.ModelSerializer):
    class Meta:
        model = ProductsInBasket
        fields = ['product', 'quantity']
        extra_kwargs = {
            'product': {'read_only': True}
        }

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value