from django.urls import path
from .views import StreamUsers, StreamUser

urlpatterns = [
    path("users/", StreamUsers.as_view(), name='stream-users'),
    path("streamuser/", StreamUser.as_view(), name='stream-user'),
]