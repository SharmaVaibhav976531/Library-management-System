from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'role')
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        user = authenticate(**data)
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials or inactive account.")
        return {'user': user}