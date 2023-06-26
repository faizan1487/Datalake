from django.urls import path
from .views import AffiliateUsers, CreateAffiliateUser, CreateAffiliateClick, UserDelete

urlpatterns = [
    path("users/", AffiliateUsers.as_view(), name='affiliate-users'),
    path("create/", CreateAffiliateUser.as_view(), name='create-affiliate-user'),
    path("clickcreate/", CreateAffiliateClick.as_view(), name='create-affiliate-click'),
    path("deleteuniqueclick/", UserDelete.as_view(), name='user-dalete'),
]