from rest_framework import serializers
from .models import Comment
from django.utils import timezone
from products.models import Product


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
