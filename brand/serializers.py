from rest_framework import serializers
from .models import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

    def get_image_url(self, instance):
        if instance.image:
            return instance.image.url
        return None


class BrandIdNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ("id", "name")