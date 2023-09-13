from django.contrib import admin
from rest_framework.serializers import ModelSerializer
from .models import Alnafi_Product,IslamicAcademy_Product, Main_Product, Course, Track, New_Alnafi_Product
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

# Register your models here.

# FOR AL-NAFI MAIN SITE PRODUCT:


class AlnafiProductAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'product_type', 'product_slug', 'plan', 'name', 'bundle_Ids', 'amount_pkr', 'amount_usd', 'amount_gbp', 'old_amount_pkr', 'old_amount_usd', 'legacy_fee_pkr', 'legacy_fee_usd',
                    'legacy_available', 'qarz_product', 'qarz_fee_pkr', 'qarz_fee_usd', 'lms_id', 'language', 'created_at', 'has_legacy_version', 'is_certificate_product', 'allow_coupon', 'courses')
    search_fields = ("id", "name", "product_slug", "language",
                     "bundle_Ids", "plan", "product_type")
    list_filter = ('created_at', "language", "product_type", "plan")


admin.site.register(Alnafi_Product, AlnafiProductAdmin)


# FOR ISLAMIC ACADEMY PRODUCT:
class IslamicAcademyProductAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ("id", "name", "product_slug", "created_at",
                    "modified_at", "type", "status", "price", "stock_status")
    search_fields = ("id", "name", "product_slug")
    list_filter = ('created_at', "type", "status", "stock_status")


admin.site.register(IslamicAcademy_Product, IslamicAcademyProductAdmin)


# FOR MAIN PRODUCTS COMBINE PRODUCT ALL TABLE IN ONE:
class MainProductAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ("id", "source", "product_name", "product_slug", "created_at", "modified_at", "product_type", "product_plan", "amount_pkr", "amount_usd", "amount_gbp", "old_amount_pkr", "old_amount_usd", "legacy_fee_pkr", "legacy_fee_usd",
                    "legacy_available", "qarz_product", "qarz_fee_pkr", "qarz_fee_usd", "lms_id", "product_language", "has_legacy_version", "is_certificate_product", "allow_coupon", "courses", "image", "bundle_ids", "status", "description", "stock_status")
    search_fields = ("product_name", "product_slug")
    list_filter = ("created_at", "source", "product_type", "product_plan",
                   "product_language", "allow_coupon", "amount_pkr", "amount_usd")


admin.site.register(Main_Product, MainProductAdmin)



# Register your models here.
class TrackAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name']
    search_fields = ('name',)
admin.site.register(Track, TrackAdmin)

class CourseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name']
    search_fields = ('name',)


admin.site.register(Course, CourseAdmin)

#For Al-Nafi New Main Site:
class NewAlnafiProductAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'product_type', 'product_slug', 'plan', 'name', 'bundle_Ids', 'amount_pkr', 'amount_usd', 'amount_gbp', 'old_amount_pkr', 'old_amount_usd', 'legacy_fee_pkr', 'legacy_fee_usd',
                    'legacy_available', 'qarz_product', 'qarz_fee_pkr', 'qarz_fee_usd', 'lms_id', 'language', 'created_at', 'has_legacy_version', 'is_certificate_product', 'allow_coupon', 'courses')
    search_fields = ("id", "name", "product_slug", "language",
                     "bundle_Ids", "plan", "product_type")
    list_filter = ('created_at', "language", "product_type", "plan")


admin.site.register(New_Alnafi_Product, AlnafiProductAdmin)