from django.contrib import admin
from django.contrib import admin
from newsletter.models import Newsletter
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateTimeRangeFilter

# Register your models here.

class NewsletterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'created_at')
    list_filter = (('created_at',DateTimeRangeFilter),)
    search_fields = ('full_name', 'phone_number', 'email')
    list_per_page = 500

admin.site.register(Newsletter, NewsletterAdmin)