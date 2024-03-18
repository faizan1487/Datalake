from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'amount', 'created_at', 'user', 'month', 'currency')
    search_fields = ('subject', 'user__email', 'month','amount','currency','created_at')  # You can customize search fields as needed
    list_filter = ('month', 'currency')  # You can add more filters as needed
