from django.contrib import admin
from django.contrib import admin
from newsletter.models import Newsletter
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateTimeRangeFilter

# Register your models here.

class NewsletterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('first_name', 'phone', 'email', 'created_at','source')
    list_filter = (('created_at',DateTimeRangeFilter),)
    search_fields = ('first', 'phone', 'email','source')
    list_per_page = 500

admin.site.register(Newsletter, NewsletterAdmin)