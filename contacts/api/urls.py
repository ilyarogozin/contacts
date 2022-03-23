from django.urls import path

from .views import create_user, create_token

app_name = 'api'

urlpatterns = [
    path('clients/create/', create_user, name='create_user'),
    path('auth/token/', create_token, name='token'),
]
