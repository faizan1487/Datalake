from django.contrib import admin
from rest_framework.serializers import ModelSerializer
from .models import AlnafiProduct
from .models import IslamicAcademyProduct
from import_export.admin import ImportExportModelAdmin


# Register your models here.

#FOR AL-NAFI MAIN SITE PRODUCT:
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
 
    list_display = ('id', "name", "productSlug", "language", "bundle_Ids", "amount_pkr", "amount_usd", "legacy_available", "legacy_fee_pkr", "legacy_fee_usd",'qarz_product', 'qarz_fee_pkr', 'qarz_fee_usd',"product_type", "plan", 'old_amount_usd', 'old_amount_pkr', 'is_certificate_product', 'allow_coupon','created_at')
    search_fields = ("id", "name", "productSlug", "language", "bundle_Ids","plan", "product_type")
    list_filter = ('created_at',"language", "product_type", "plan")

admin.site.register(AlnafiProduct, ProductAdmin)

#FOR ISLAMIC ACADEMY PRODUCT:
class IslamicAcademyProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "slug", "date_created", "date_modified", "type", "status", "price", "stock_status")
    search_fields = ("id", "name", "slug")
    list_filter = ('date_created', "type", "status", "stock_status")

admin.site.register(IslamicAcademyProduct, IslamicAcademyProductAdmin)


