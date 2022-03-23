from django.urls import path

from .views import create_token, create_user, get_match

app_name = 'api'

urlpatterns = [
    path('clients/create/', create_user, name='create_user'),
    path('auth/token/', create_token, name='token'),
    path('clients/<int:user_id>/match/', get_match, name='get_match'),
]
