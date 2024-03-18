from django.urls import path
from .views import Subscribers, CreateNewsletter, NewsletterUser



urlpatterns = [
    path("subscribers/", Subscribers.as_view(), name='subscribers'),
    path("create/", CreateNewsletter.as_view(), name='create-newsletter'),
    path("newsletteruser/", NewsletterUser.as_view(), name='newsletter-user'),
]