# from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authentication import authenticate
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password',
                  'first_name', 'last_name', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class LoginSerialiser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print('data = ', data)
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError('Incorrect Credentials')
