from django.urls import path
from .views import Subscribers, CreateNewsletter



urlpatterns = [
    path("subscribers/", Subscribers.as_view(), name='subscribers'),
    path("create/", CreateNewsletter.as_view(), name='create-newsletter'),
]