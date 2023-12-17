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

    def validate(self, data):
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        product_db = Product.objects.filter(id=product_id).first()

        if not product_db:
            raise serializers.ValidationError('Продукт с данным ключем отсутсвует')

        if quantity > product_db.quantity:
            raise serializers.ValidationError('Запрошенное количество превышает доступное количество продукта.')
        return data

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
        fields = ['id', 'created_at', 'updated_at', 'payment_status', 'order_status', 'total_cost', 'order_items']

    def get_total_cost(self, obj):
        return obj.total_cost


class OrderWriteSerializers(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = OrderedProductsSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "total_price",
            'user',
            'payment_status',
            'order_status',
            'created_at',
            'updated_at',
            'price',
            'quantity'
        ]
        read_only_fields = ['total_price', 'payment_status', 'order_status']

    def create(self, validated_data):
        orders_data = validated_data.pop('order_items')
        status_db = PaymentStatus.objects.get(status="cash")
        order = Order.objects.create(payment_status=status_db, **validated_data)

        for order_data in orders_data:
            product_id = order_data['product_id']
            product = Product.objects.filter(pk=product_id).first()
            product.quantity = product.quantity - order_data['quantity']
            product.save()
            OrderedProducts.objects.create(order=order, **order_data)

        return order

