from django_filters.rest_framework import DjangoFilterBackend
from geopy.distance import great_circle

from .models import User


def get_distance_between_two_points(coords1, coords2):
    return great_circle(coords1, coords2).km


class UserFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if ('first_name' in request.GET
           or 'last_name' in request.GET
           or 'gender' in request.GET):
            return super().filter_queryset(request, queryset, view)
        users = queryset
        max_range = request.GET.get('range')
        if max_range:
            filtered_users = set()
            coords1 = (request.user.latitude, request.user.longitude)
            max_distance = int(max_range)
            for user in users:
                coords2 = (user.latitude, user.longitude)
                distance = get_distance_between_two_points(
                    coords1, coords2
                )
                if distance < max_distance:
                    filtered_users.add(user.id)
            return User.objects.filter(id__in=filtered_users)
        return queryset
