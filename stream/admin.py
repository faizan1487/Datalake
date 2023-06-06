from django.contrib import admin
from stream.models import StreamUser
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateTimeRangeFilter

# Register your models here.

class StreamUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('first_name','last_name', 'phone', 'email','country', 'created_at')
    list_filter = (('created_at',DateTimeRangeFilter),)
    search_fields = ('first_namme', 'phone', 'email')
    list_per_page = 500

admin.site.register(StreamUser, StreamUserAdmin)