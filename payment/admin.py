from django.contrib import admin
from .models import Payment
# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = [('payment_source', 'first_name', 'last_name', 'email', 'enrollment_name', 'enrollment_creation_date', 'enrollment_expiry_date', 'payment_date')]
    per_page = 500

admin.site.register(Payment)