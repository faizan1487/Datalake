from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from .models import Scan
# Register your models here.    

#For Navbar:
  

#For Stripe Payments:
class ScanAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'scan_type', 'scan_date', 'severity','scan_progress','assigned_to')
    list_filter = ('scan_type', 'severity', 'scan_progress')
    search_fields = ('id', 'scan_type')  # Assuming the ForeignKey field is related to the TeamMember model

admin.site.register(Scan, ScanAdmin)
