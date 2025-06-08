from rest_framework import serializers
from .models import TodoModel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Serializer for the TodoModel
class TodoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModel
        # Fields to include in the serialized output
        fields = ['id', 'title', 'description', 'completed']


# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    # Password is write-only to prevent it from being returned in responses
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # Fields required for registration
        fields = ['username', 'email', 'password']
    
    # Validates if the username already exists in the system
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    # Creates a new user using Django's create_user method
    def create(self, validatedData):
        return User.objects.create_user(**validatedData)


# Serializer for user login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # Validates the username and password combination
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user  # Attach the user object to the validated data
        return data
