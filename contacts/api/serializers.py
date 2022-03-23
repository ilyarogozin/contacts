from rest_framework import serializers

from .models import GENDERS


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=200)


class UserSerializer(serializers.Serializer):
    avatar = serializers.ImageField()
    gender = serializers.ChoiceField(choices=GENDERS, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)
    country = serializers.CharField(max_length=100, required=True)
