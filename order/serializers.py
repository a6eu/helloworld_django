from rest_framework import serializers
from .models import *
from products.serializers import ProductReadSerializer


class OrderedProductsSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    cost = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderedProducts
        fields = ['product_id', 'quantity', 'cost']

    def get_cost(self, obj):
        return obj.cost


class OrderDetailProductsSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    quantity = serializers.IntegerField()
    cost = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderedProducts
        fields = ['product', 'quantity', 'cost']

    def get_cost(self, obj):
        return obj.cost


class OrderListSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField(read_only=True)
    order_items = OrderDetailProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'updated_at', 'status', 'total_cost', 'order_items']

    def get_total_cost(self, obj):
        return obj.total_cost


class OrderWriteSerializers(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = OrderedProductsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['product', "total_price", 'user', 'status', 'created_at', 'updated_at', 'price', 'quantity']
        read_only_fields = ['total_price', 'status']

    def create(self, validated_data):
        orders_data = validated_data.pop('order_items')
        status_db = PaymentStatus.objects.get(status="cash")
        order = Order.objects.create(status=status_db, **validated_data)

        for order_data in orders_data:
            OrderedProducts.objects.create(order=order, **order_data)
        return order

