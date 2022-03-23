from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'email', 'gender',
        'country', 'city', 'avatar'
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('country', 'city')
    empty_value_display = '-пусто-'
