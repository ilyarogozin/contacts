from rest_framework import serializers
from imagekit.lib import Image

from .models import GENDERS

DEFAULT_AVATAR = Image.open('default_avatar.jpeg')


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=200)


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=150)
    avatar = serializers.ImageField(default=DEFAULT_AVATAR)
    gender = serializers.ChoiceField(choices=GENDERS)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    country = serializers.CharField(max_length=100, default='Russia')
    city = serializers.CharField(max_length=100, default='Moscow')
