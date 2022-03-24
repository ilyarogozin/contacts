from imagekit.lib import Image
from rest_framework import serializers

from .models import User

DEFAULT_AVATAR = Image.open('default_avatar.jpeg')


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=200)


class UserSerializer(serializers.Serializer):
    avatar = serializers.ImageField(default=DEFAULT_AVATAR)
    country = serializers.CharField(max_length=100, default='Russia')
    city = serializers.CharField(max_length=100, default='Moscow')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'avatar', 'gender', 'first_name',
            'last_name', 'email', 'country', 'city'
        )
