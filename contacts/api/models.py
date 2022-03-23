from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

GENDERS = [
    ('male', 'Мужчина'),
    ('female', 'Женщина'),
]


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        help_text=(
            'Обязательное. 150 символов или меньше. '
            'Только буквы, цифры и "@/./+/-/_".'
        ),
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует',
        },
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=150, required=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150, required=True
    )
    email = models.EmailField(
        verbose_name='Почта', max_length=254, unique=True
    )
    avatar = models.ImageField()
    gender = models.CharField(
        verbose_name='Пол', choices=GENDERS, max_length=7
    )
    longitude = models.FloatField(
        verbose_name='Долгота', max_length=100, default=37.6174943
    )
    latitude = models.FloatField(
        verbose_name='Широта', max_length=100, default=55.7504461
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
