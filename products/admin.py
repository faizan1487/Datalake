from django.contrib import admin
from rest_framework.serializers import ModelSerializer
from .models import AlnafiProduct
from import_export.admin import ImportExportModelAdmin


# Register your models here.
#For Product:
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("name", "productSlug", "language", "bundle_Ids", "amount_pkr", "amount_usd", "legacy_available", "legacy_fee_pkr", "legacy_fee_usd","product_type", "plan", 'old_amount_usd', 'old_amount_pkr','created_at')
    search_fields = ("name", "productSlug", "language", "bundle_Ids","plan")
    list_filter = ('created_at',"language", "product_type", "plan")

admin.site.register(AlnafiProduct, ProductAdmin)