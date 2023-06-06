from django.urls import path
from .views import StreamUsers

urlpatterns = [
    path("users/", StreamUsers.as_view(), name='stream-users'),
]