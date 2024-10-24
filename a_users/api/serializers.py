# your_app/api/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)  # Expect email in the request

    # We override the validation method to use email instead of username
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Try to get the user based on email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "No user with this email."})

        # Authenticate the user manually
        user = authenticate(username=user.username, password=password)
        if user is None:
            raise serializers.ValidationError({"password": "Incorrect password."})

        # Add the username to the attrs to satisfy the parent validation
        attrs['username'] = user.username
        return super().validate(attrs)
