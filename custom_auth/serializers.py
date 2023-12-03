# serializers.py
from rest_framework import serializers
from .models import UserProfile

from django.contrib.auth.hashers import make_password


class EmailPhoneLoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        user = UserProfile.objects.create_user(**validate_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'gender', 'birth_day', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.birth_day = validated_data.get('birth_day', instance.birth_day)

        password = validated_data.get('password', None)
        if password is not None:
            instance.password = make_password(password)

        instance.save()
        return instance
