from rest_framework import serializers
from category.models import Category


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
        fields = ("id", "categoryId", "name", "children")

    def get_image_url(self, instance):
        if instance.image:
            return instance.image.url
        return None


class CategoryNameIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "categoryId")