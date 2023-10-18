from django.urls import path
from .views import (SearchPayments, GetStripePayments,GetUBLIPGPayments, AlnafiPayment,
                    RenewalPayments,GetEasypaisaPayments,NoOfPayments,RenewalNoOfPayments,
                    PaymentValidation,PaymentValidationNew,MainPaymentAPIView,UBLManualPayment,TotalNoOfPayments,
                    ActivePayments,ProductAnalytics, NewAlnafiPayment)
from payment.webhooks import enrollment_created_webhook

urlpatterns = [
    path("enrollmentwebhook/", enrollment_created_webhook),

    # path("deletepayment/", PaymentDelete.as_view(), name='payment-dalete'),
    path("alnafipayment/", AlnafiPayment.as_view(), name='alnafi-payment'),
    path("newalnafipayment/", NewAlnafiPayment.as_view(), name='new-alnafi-payment'),
    path("ublmanualpayment/", UBLManualPayment.as_view(), name='ubl-manual-payment'),
    path("ublipgpayment/", GetUBLIPGPayments.as_view(), name='ubl-manual-payment'),
    path("easypaisa/", GetEasypaisaPayments.as_view(), name='easypaisa'), #For all easypaisa Payments
    path("stripe/", GetStripePayments.as_view(), name='all'),  #For all stripe payemnts

    path('createpayments/', MainPaymentAPIView.as_view(), name='main-payments-api'),

    path("searchpayment/", SearchPayments.as_view(), name='search-payments'),
    path("searchalnafipayment/", RenewalPayments.as_view(), name='search-alnafi-payments'),
    path("searchactivepayment/", ActivePayments.as_view(), name='search-active-payments'),
    path("paymentvalidation/", PaymentValidation.as_view(), name='payment-validation'),
    path("paymentvalidationnew/", PaymentValidationNew.as_view(), name='payment-validation'),

    path("nofpayments/", NoOfPayments.as_view(), name='no-of-payments'),
    path("totalpayments/", TotalNoOfPayments.as_view(), name='totla-payments'),
    path("nofrenewalpayments/", RenewalNoOfPayments.as_view(), name='no-of-renewal-payments'),

    path("productanalytics/", ProductAnalytics.as_view(), name='product-analytics'),
]