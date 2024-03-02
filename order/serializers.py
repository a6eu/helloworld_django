from rest_framework import serializers, status
from rest_framework.response import Response

from .models import *
from products.serializers import ProductReadSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = ['status',]


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
    payment_status = PaymentSerializer(read_only=True)
    order_items = OrderDetailProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'updated_at', 'payment_status', 'order_status', 'total_cost', 'order_items']

    @staticmethod
    def get_total_cost(obj):
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

            'quantity'
        ]
        read_only_fields = ['total_price', 'payment_status', 'order_status']

    def create(self, validated_data):
        orders_data = validated_data.pop('order_items')
        status_db = PaymentStatus.objects.get(status="Cash")
        order = Order.objects.create(payment_status=status_db, **validated_data)

        for order_data in orders_data:
            product_id = order_data['product_id']
            product = Product.objects.filter(pk=product_id).first()
            product.quantity = product.quantity - order_data['quantity']
            product.save()
            OrderedProducts.objects.create(order=order, **order_data)

        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['order_status', 'id']

    def get_id(self, obj):
        request = self.context.get('request')
        if request:
            return request.parser_context['kwargs'].get('pk')
        return None

    def update(self, instance, validated_data):
        instance.order_status = validated_data.pop('order_status')
        instance.save()
        return Response(status=status.HTTP_200_OK)