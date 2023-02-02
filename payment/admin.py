from django.contrib import admin
from .models import Payment
# Register your models here.


# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('payment_source', 'first_name', 'last_name', 'email', 'enrollment_name', 'enrollment_creation_date', 'enrollment_expiry_date', 'payment_date')
#     per_page = 500
#     search_fields = ('payment_souce','email')

# admin.site.register(Payment,PaymentAdmin)     

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id','name', 'email', 'phone', 'product', 'amount', 'created', 'status', 'currency', 'source', 'description', 'address')
    per_page = 500
    search_fields = ('email',)

admin.site.register(Payment,PaymentAdmin)     