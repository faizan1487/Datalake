from django.urls import path
from .views import (AffiliateUsers, CreateAffiliateUser, CreateAffiliateClick, UserDelete, 
                    UpdateAffiliateUser, CreateAffiliateLead, CreateCommission)

urlpatterns = [
    path("users/", AffiliateUsers.as_view(), name='affiliate-users'),
    path("create/", CreateAffiliateUser.as_view(), name='create-affiliate-user'),
    path("createlead/", CreateAffiliateLead.as_view(), name='affiliate-lead'),
    path("clickcreate/", CreateAffiliateClick.as_view(), name='create-affiliate-click'),
    path("createcommission/", CreateCommission.as_view(), name='create-commission'),
    path("deleteuniqueclick/", UserDelete.as_view(), name='user-dalete'),

    path("affiliateuser/", UpdateAffiliateUser.as_view(), name='affiliate-user'),
]