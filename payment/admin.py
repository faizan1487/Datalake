from django.contrib import admin
from .models import UBL_Manual_Payment,NavbarLink,AlNafi_Payment,UBL_IPG_Payment,Easypaisa_Payment,Stripe_Payment
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter


# Register your models here.    

#For Navbar:
class NavbarLinkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'path')

admin.site.register(NavbarLink,NavbarLinkAdmin)     

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


#For MainSite(Al-Nafi) Payments:
class AlNafiPaymentsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['payment_id', 'customer_email', 'product_name', 'amount_pkr', 'amount_usd', 'order_datetime', 'expiration_datetime', 'source', 'order_id', 'date_of_activation', 'created_at', 'qarz', 'remarks', 'payment_proof', 'send_invoice', 'pk_invoice_number', 'us_invoice_number', 'sponsored', 'coupon_code', 'is_upgrade_payment', 'affiliate']
    search_fields = ('payment_id', 'customer_email', 'order_datetime', 'expiration_datetime','product_name', 'order_id', "created_at","pk_invoice_number","us_invoice_number" )
    list_filter = ("source", 'order_datetime', 'expiration_datetime',"sponsored")
    
admin.site.register(AlNafi_Payment, AlNafiPaymentsAdmin)   

    
#For UBL Manual Payments:
class UBLManualPaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['candidate_name', 'depositor_name', 'customer_email', 'phone', 'amount', 'product_name', 'status', 'order_datetime', 'activation_datetime', 'payment_channel', 'transaction_id', 'source', 's3_file_url', 's3_file_name']
    search_fields = ('candidate_name', 'depositor_name', 'customer_email', 'phone', 'transaction_id')
    list_filter = ('status','source', 'order_datetime')

admin.site.register(UBL_Manual_Payment, UBLManualPaymentAdmin)