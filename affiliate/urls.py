from django.urls import path
from .views import (CreateAffiliateUser, CreateAffiliateClick, UserDelete, 
                    UpdateAffiliateUser, CreateAffiliateLead, CreateCommission,GetAffiliateUser,AffiliateAnalytics)

urlpatterns = [
    path("create/", CreateAffiliateUser.as_view(), name='create-affiliate-user'),
    path("createlead/", CreateAffiliateLead.as_view(), name='affiliate-lead'),
    path("clickcreate/", CreateAffiliateClick.as_view(), name='create-affiliate-click'),
    path("createcommission/", CreateCommission.as_view(), name='create-commission'),
    path("deleteuniqueclick/", UserDelete.as_view(), name='user-dalete'),

    path("affiliateuser/", UpdateAffiliateUser.as_view(), name='affiliate-user'),
    path("getaffiliateusers/", GetAffiliateUser.as_view(), name='get-affiliate-users'),
    path("getaffiliateanalytics/", AffiliateAnalytics.as_view(), name='get-affiliate-analytics'),
]