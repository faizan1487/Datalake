from django.urls import path
from .views import (SearchPayments, GetStripePayments,GetUBLIPGPayments, AlnafiPayment,
                    RenewalPayments,GetEasypaisaPayments,NoOfPayments,RenewalNoOfPayments,
                    PaymentValidationNew,MainPaymentAPIView,UBLManualPayment,TotalNoOfPayments,
                    ActivePayments,ProductAnalytics, NewAlnafiPayment,Renewal_Leads, LeadDataAPIView,ExpiryPayments,UploadLeads,NewPayments,CommisionData, Roidata,UnpaidNewAlnafiPayment,UnpaidSearchPayments)
from payment.webhooks import enrollment_created_webhook

urlpatterns = [
    path('suppport/', LeadDataAPIView.as_view()),
    path('upload-renewal-leads/', Renewal_Leads.as_view(), name='renewal-leads'),
    path("enrollmentwebhook/", enrollment_created_webhook),

    # path("deletepayment/", PaymentDelete.as_view(), name='payment-dalete'),
    path("alnafipayment/", AlnafiPayment.as_view(), name='alnafi-payment'),
    path("newalnafipayment/", NewAlnafiPayment.as_view(), name='new-alnafi-payment'),
    path("unpaidnewalnafipayment/", UnpaidNewAlnafiPayment.as_view(), name='unpaid-new-alnafi-payment'),
    path("ublmanualpayment/", UBLManualPayment.as_view(), name='ubl-manual-payment'),
    path("ublipgpayment/", GetUBLIPGPayments.as_view(), name='ubl-manual-payment'),
    path("easypaisa/", GetEasypaisaPayments.as_view(), name='easypaisa'), #For all easypaisa Payments
    path("stripe/", GetStripePayments.as_view(), name='all'),  #For all stripe payemnts

    path('createpayments/', MainPaymentAPIView.as_view(), name='main-payments-api'),

    path("searchpayment/", SearchPayments.as_view(), name='search-payments'),
    path("searchunpaidpayment/", UnpaidSearchPayments.as_view(), name='unpaid-search-payments'),


    path('expiry-payments/', ExpiryPayments.as_view(), name= 'expiry-payments-in-range'),
    path('new-payments/', NewPayments.as_view(), name= 'new-payments'),
    path("searchalnafipayment/", RenewalPayments.as_view(), name='search-alnafi-payments'),
    path("searchactivepayment/", ActivePayments.as_view(), name='search-active-payments'),
    # path("paymentvalidation/", PaymentValidation.as_view(), name='payment-validation'),
    path("paymentvalidation/", PaymentValidationNew.as_view(), name='payment-validation'),

    path("nofpayments/", NoOfPayments.as_view(), name='no-of-payments'),
    path("totalpayments/", TotalNoOfPayments.as_view(), name='totla-payments'),
    path("nofrenewalpayments/", RenewalNoOfPayments.as_view(), name='no-of-renewal-payments'),


    path("productanalytics/", ProductAnalytics.as_view(), name='product-analytics'),
    path("upload_support_leads/", LeadDataAPIView.as_view(), name='support-leads'),
    path("upload_leads/", UploadLeads.as_view(), name='upload-leads'),
    path("commission/", CommisionData.as_view()),
    path("roi_data/", Roidata.as_view())

]