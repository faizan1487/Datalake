from django.urls import path
from .views import AffiliateUsers

urlpatterns = [
    path("users/", AffiliateUsers.as_view(), name='affiliate-users'),
]