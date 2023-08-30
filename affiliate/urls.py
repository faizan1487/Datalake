from django.urls import path
from .views import (CreateAffiliateUser, CreateAffiliateClick, UserDelete, 
                    UpdateAffiliateUser, CreateAffiliateLead, CreateCommission,
                    GetAffiliateUsersEmails,AffiliateAnalytics,GetAffiliateUser,AffiliateProducts,GetAffiliateData)

urlpatterns = [
    path("create/", CreateAffiliateUser.as_view(), name='create-affiliate-user'),
    path("createlead/", CreateAffiliateLead.as_view(), name='affiliate-lead'),
    path("clickcreate/", CreateAffiliateClick.as_view(), name='create-affiliate-click'),
    path("createcommission/", CreateCommission.as_view(), name='create-commission'),
    path("deleteuniqueclick/", UserDelete.as_view(), name='user-dalete'),

    path("updateaffiliateuser/", UpdateAffiliateUser.as_view(), name='affiliate-user'),
    path("getaffiliateusers/", GetAffiliateUsersEmails.as_view(), name='get-affiliate-users-emails'),
    path("getaffiliateanalytics/", AffiliateAnalytics.as_view(), name='get-affiliate-analytics'),
    path("affiliateuserdetails/<int:id>/", GetAffiliateUser.as_view(), name='get-affiliate-user-by-id'),
    path("affiliateproducts/", AffiliateProducts.as_view(), name='get-affiliate-products'),
    path("getaffiliatedata/", GetAffiliateData.as_view(), name='get-affiliate-data'),
]