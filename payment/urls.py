
from django.urls import path
from .views import GetUserDetails, GetEasyPaisaUserDetails, GetStripeUserDetails, GetUblUserDetails, GetAllUserDetails, SearchUser

urlpatterns = [
    path("",GetAllUserDetails.as_view(),name='get_all_users_details'),
    path("/payment",GetUserDetails.as_view(),name='get_user_details'),
    path("/easypaisa",GetEasyPaisaUserDetails.as_view(),name='get_easypaisa_users_details'),
    path("/stripe",GetStripeUserDetails.as_view(),name='get_stripe_users_details'),
    path("/ubl",GetUblUserDetails.as_view(),name='get_ubl_users_details'),
    # path('/search/', SearchUser.as_view()),
]