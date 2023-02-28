from django.contrib import admin
from .models import Payment
from .models import Easypaisa_Payment
from .models import UBL_IPG_Payment
from .models import Product
from import_export.admin import ImportExportModelAdmin

# Register your models here.


# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('payment_source', 'first_name', 'last_name', 'email', 'enrollment_name', 'enrollment_creation_date', 'enrollment_expiry_date', 'payment_date')
#     per_page = 500
#     search_fields = ('payment_souce','email')

# admin.site.register(Payment,PaymentAdmin)     

#For Stripe Payments:
class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('payment_id','name', 'email', 'phone', 'product', 'amount', 'created', 'status', 'currency', 'source', 'description', 'address')
    per_page = 500
    search_fields = ('email',)

admin.site.register(Payment,PaymentAdmin)     

#For Easypaisa Payments:
class EasypaisaPaymentsAdmin(admin.ModelAdmin):
    list_display = ['ops_id','product_name','order_id','transaction_id','order_datetime','customer_msidn','customer_email','amount_pkr','status','source','credit_card','bin_bank_name','fee_pkr',	'fed_pkr','error_reason','token_paid_datetime']
    per_page = 500
    search_fields = ('customer_email',)

admin.site.register(Easypaisa_Payment, EasypaisaPaymentsAdmin)


#For UBL IPG Payments:
class UBLIPGPaymentsAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'customer_email', 'card_mask', 'product_name', 'order_datetime', 'order_id', 'amount', 'captured', 'reversed', 'refund', 'approval_code', 'source', 'status']
    per_page = 500
    search_fields = ('customer_email','card_mask',)

admin.site.register(UBL_IPG_Payment, UBLIPGPaymentsAdmin)   


#For Product:
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("name", "productSlug", "language", "bundle_Ids", "amount_pkr", "amount_usd", "legacy_available", "legacy_fee_pkr", "legacy_fee_usd","product_type", "plan", 'old_amount_usd', 'old_amount_pkr','created_at')
    search_fields = ("name", "productSlug", "language", "bundle_Ids","plan")
    list_filter = ('created_at',"language", "product_type", "plan")

admin.site.register(Product, ProductAdmin)