from rest_framework import serializers, status

from .models import News


class NewsCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'created_by']


class NewsListSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = '__all__'


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'content', 'updated_at', 'created_at', 'image']
        read_only_fields = ['created_at']

