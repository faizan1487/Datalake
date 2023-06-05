from django.urls import path
from .views import Subscribers



urlpatterns = [
    path("subscribers/", Subscribers.as_view(), name='subscribers'),
]