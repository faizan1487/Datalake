from django.contrib import admin
from .models import Stripe_Payment
from .models import Easypaisa_Payment
from .models import UBL_IPG_Payment
from import_export.admin import ImportExportModelAdmin

# Register your models here.    

#For Stripe Payments:
class StripePaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('payment_id','name', 'customer_email', 'phone', 'product_name', 'amount', 'order_datetime', 'status', 'currency', 'source', 'description', 'address')
    search_fields = ('customer_email','payment_id','name', 'phone','product_name')
    list_filter = ('order_datetime', 'status', 'currency', 'source')

admin.site.register(Stripe_Payment,StripePaymentAdmin)     

#For Easypaisa Payments:
class EasypaisaPaymentsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['ops_id','product_name','order_id','transaction_id','order_datetime','customer_msidn','customer_email','amount','status','source','credit_card','bin_bank_name','fee_pkr',	'fed_pkr','error_reason','token_paid_datetime']
    search_fields = ('customer_email','ops_id', 'product_name', 'order_id', 'transaction_id', 'customer_msidn', 'credit_card')
    list_filter = ('order_datetime', 'status','source', 'token_paid_datetime')

admin.site.register(Easypaisa_Payment, EasypaisaPaymentsAdmin)


#For UBL IPG Payments:
class UBLIPGPaymentsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['transaction_id', 'customer_email', 'card_mask', 'product_name', 'order_datetime', 'order_id', 'amount', 'captured', 'reversed', 'refund', 'approval_code', 'source', 'status']
    search_fields = ('customer_email','card_mask', 'transaction_id','product_name', 'order_id', 'approval_code')
    list_filter = ('order_datetime', 'source', 'status')

admin.site.register(UBL_IPG_Payment, UBLIPGPaymentsAdmin)   