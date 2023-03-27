from django.urls import path
from .views import SearchPayments, GetStripePayments, GetUBLPayments, AlnafiPayment,SearchAlNafiPayments

urlpatterns = [
    path("alnafipayment/", AlnafiPayment.as_view(), name='alnafi-payment'),
    path("searchpayment/", SearchPayments.as_view(), name='search-payments'),
    path("searchalnafipayment/", SearchAlNafiPayments.as_view(), name='search-alnafi-payments'),
    path("stripe/", GetStripePayments.as_view(), name='all'),  #For all stripe payemnts
    path("ubl/", GetUBLPayments.as_view(), name='ubl'), #For all UBL Payments
]