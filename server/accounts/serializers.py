# accounts/serializers.py

from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('login', 'password', 'password2', 'name', 'surname')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Hasła nie są identyczne."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomAuthTokenSerializer(serializers.Serializer):
    login = serializers.CharField(label="Login")
    password = serializers.CharField(label="Hasło", style={'input_type': 'password'})

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        if login and password:
            user = authenticate(login=login, password=password)
            if not user:
                raise serializers.ValidationError("Nieprawidłowe dane uwierzytelniające.", code='authorization')
        else:
            raise serializers.ValidationError("Należy podać login i hasło.", code='authorization')

        attrs['user'] = user
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Nowe hasła nie są identyczne."})
        return attrs

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('login', 'name', 'surname')

    def validate_login(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(login=value).exists():
            raise serializers.ValidationError("Użytkownik z tym loginem już istnieje.")
        return value

    def update(self, instance, validated_data):
        instance.login = validated_data.get('login', instance.login)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.save()
        return instance
