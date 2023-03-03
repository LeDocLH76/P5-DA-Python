from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.authentication import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password',
                  'first_name', 'last_name', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def validate_password(self, data):
        """
            Validate password with AUTH_PASSWORD_VALIDATORS [] from settings.
        """
        user = get_user_model()(
            username=self.initial_data['username'],
            password=self.initial_data['password'],
            email=self.initial_data['email'],
            first_name=self.initial_data['first_name'],
            last_name=self.initial_data['last_name'],
        )
        errors = False
        try:
            password_validation.validate_password(
                password=user.password,
                user=user
            )
        except ValidationError as err:
            errors = err.messages
        if errors:
            raise serializers.ValidationError(errors)
        return super(RegisterSerializer, self).validate(data)

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class LoginSerialiser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError('Incorrect Credentials')
