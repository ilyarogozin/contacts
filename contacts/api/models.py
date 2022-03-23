from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from imagekit.lib import Image
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

GENDERS = [
    ('male', 'Мужчина'),
    ('female', 'Женщина'),
]
WATERMARK = (
    Image.open('watermark.jpeg').convert('RGBA')
)


class Watermark(object):
    def process(self, image, watermark=WATERMARK):
        image.paste(
            watermark,
            (0, 0, watermark.size[0], watermark.size[0]),
            watermark
        )
        return image


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
        verbose_name='Имя', max_length=150, blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150, blank=False
    )
    email = models.EmailField(
        verbose_name='Почта', max_length=254, unique=True, blank=False
    )
    avatar = ProcessedImageField(
        upload_to='avatars',
        processors=[ResizeToFill(100, 100), Watermark()],
        format='JPEG',
        options={'quality': 256}
    )
    gender = models.CharField(
        verbose_name='Пол', choices=GENDERS, max_length=7
    )
    longitude = models.FloatField(
        verbose_name='Долгота', max_length=100, default=37.6174943
    )
    latitude = models.FloatField(
        verbose_name='Широта', max_length=100, default=55.7504461
    )
    likes = models.ManyToManyField('User', blank=True, related_name="like")
    country = models.CharField(
        verbose_name='Страна', max_length=100, blank=True
    )
    city = models.CharField(verbose_name='Город', max_length=100, blank=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
