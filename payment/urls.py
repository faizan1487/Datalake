from django.urls import path
from .views import SearchPayments,GetStripePayments,GetUBLPayments,Import_csv

urlpatterns = [
    # path("",GetAllUserDetails.as_view(),name='get_all_users_details'),
    # path("easypaisa",GetEasyPaisaUserDetails.as_view(),name='get_easypaisa_users_details'),
    # path("stripe",GetStripeUserDetails.as_view(),name='get_stripe_users_details'),
    # path("ubl",GetUblUserDetails.as_view(),name='get_ubl_users_details'),
    path('import-csv/', Import_csv.as_view(), name='import_csv'),
    path("searchpayment/", SearchPayments.as_view(), name='search_payments'),
    path("stripe/", GetStripePayments.as_view(), name='all'),  #For all stripe payemnts
    path("ubl/", GetUBLPayments.as_view(), name='ubl'), #For all UBL Payments
]