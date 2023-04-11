from django.urls import path
from .views import (SearchPayments, GetUBLPayments, AlnafiPayment,SearchAlNafiPayments,GetEasypaisaPayments,
                    NoOfPayments,RenewalNoOfPayments)
from payment.webhooks import enrollment_created_webhook

urlpatterns = [
    path("enrollmentwebhook/", enrollment_created_webhook),
    path("alnafipayment/", AlnafiPayment.as_view(), name='alnafi-payment'),
    path("searchpayment/", SearchPayments.as_view(), name='search-payments'),
    path("searchalnafipayment/", SearchAlNafiPayments.as_view(), name='search-alnafi-payments'),
    path("nofpayments/", NoOfPayments.as_view(), name='no-of-payments'),
    path("nofrenewalpayments/", RenewalNoOfPayments.as_view(), name='no-of-renewal-payments'),
    # path("stripe/", GetStripePayments.as_view(), name='all'),  #For all stripe payemnts
    path("ubl/", GetUBLPayments.as_view(), name='ubl'), #For all UBL Payments
    path("easypaisa/", GetEasypaisaPayments.as_view(), name='easypaisa'), #For all easypaisa Payments
]