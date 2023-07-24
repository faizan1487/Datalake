from django.urls import path
from .views import StreamUsers, UpdateStreamUser

urlpatterns = [
    path("users/", StreamUsers.as_view(), name='stream-users'),
    path("streamuser/", UpdateStreamUser.as_view(), name='stream-user'),
]