from django.contrib import admin
from .models import AffiliateUser, AffiliateUniqueClick, AffiliateLead
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateTimeRangeFilter

# Register your models here.

class AffiliateUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('first_name','last_name', 'phone', 'email','country', 'created_at')
    list_filter = (('created_at',DateTimeRangeFilter),)
    search_fields = ('first_name', 'phone', 'email')
    list_per_page = 500

admin.site.register(AffiliateUser, AffiliateUserAdmin)

class AffiliateLeadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('affiliate','email','first_name','last_name', 'contact','country', 'created_at')
    list_filter = (('created_at',DateTimeRangeFilter),)
    search_fields = ('first_name', 'phone', 'email')
    list_per_page = 500

admin.site.register(AffiliateLead, AffiliateLeadAdmin)


class AffiliateUniqueClickAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('ip','page_url', 'affiliate_id', 'pkr_price','usd_price','created_at')
    list_filter = (('created_at',DateTimeRangeFilter),)
    search_fields = ('ip','page_url', 'affiliate_id', 'pkr_price','usd_price')
    list_per_page = 500

admin.site.register(AffiliateUniqueClick, AffiliateUniqueClickAdmin)