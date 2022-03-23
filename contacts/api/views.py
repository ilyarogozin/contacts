from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import get_object_or_404
from geopy.geocoders import Nominatim
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
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
MUTUAL_SYMPATHY = 'У вас взаимная симпатия!'
YOU_LIKED = 'Вы понравились {name}! Почта участника: {email}'
EMAIL_NOT_SENT = 'Email не был отправлен: {error}'


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


def send_mutual_sympathy(recipient, name, email):
    try:
        send_mail(
            subject=MUTUAL_SYMPATHY, recipient_list=[recipient],
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=YOU_LIKED.format(name=name, email=email),
            fail_silently=False
        )
    except BadHeaderError as error:
        raise BadHeaderError(EMAIL_NOT_SENT.format(error=error))


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_match(request, user_id):
    user = request.user
    like = get_object_or_404(User, id=user_id)
    if like in user.like.all():
        return Response({'alert': 'you have already liked this user'})
    user.like.set(User.objects.filter(id=user_id))
    likes = like.like.all()
    if user not in likes:
        return Response(status=status.HTTP_200_OK)
    name_user = user.first_name
    email_user = user.email
    name_matching = like.first_name
    email_matching = like.email
    send_mutual_sympathy(email_matching, name_user, email_user)
    send_mutual_sympathy(email_user, name_matching, email_matching)
    data = {'email of your matching': email_matching}
    return Response(data, status=status.HTTP_200_OK)
