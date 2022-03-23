from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.core.mail import BadHeaderError, send_mail
from geopy.geocoders import Nominatim
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import ConfirmationCodeSerializer, UserSerializer

ACTIVATE = 'Активируйте свой аккаунт.'
CONFIRMATION_CODE = (
    'Ваш код подтверждения: {confirmation_code}\n'
    'Передайте эндпоинту http://127.0.0.1:8000/api/auth/token/\n'
    'свои "username" и "confirmation_code" для получения токена'
)
USERNAME_ALREADY_EXISTS = 'Пользователь с таким username уже существует!'
EMAIL_ALREADY_EXISTS = 'Пользователь с таким email уже существует!'


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email').lower()
    try:
        user = User.objects.get(username=username, email=email)
    except User.DoesNotExist:
        if User.objects.filter(username=username).exists():
            raise ValidationError(USERNAME_ALREADY_EXISTS)
        if User.objects.filter(email=email).exists():
            raise ValidationError(EMAIL_ALREADY_EXISTS)
        nom = Nominatim(user_agent='my_app')
        city = serializer.validated_data.get('city')
        country = serializer.validated_data.get('country')
        address = nom.geocode(f'{ city } { country }')
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=serializer.validated_data.get('first_name'),
            last_name=serializer.validated_data.get('last_name'),
            avatar=serializer.validated_data.get('avatar'),
            gender=serializer.validated_data.get('gender'),
            longitude=address.longitude,
            latitude=address.latitude
        )
    user.set_password(BaseUserManager().make_random_password())
    user.save()
    confirmation_code = user.password
    try:
        send_mail(
            subject=ACTIVATE, recipient_list=[email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=CONFIRMATION_CODE.format(
                confirmation_code=confirmation_code,
            ),
            fail_silently=False
        )
    except BadHeaderError as error:
        raise BadHeaderError(f'Email не был отправлен: { error }')
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    if not User.objects.filter(username=username).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = User.objects.get(username=username)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if user.password == confirmation_code:
        token = str(RefreshToken.for_user(user).access_token)
        return Response(data={'token': token}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
