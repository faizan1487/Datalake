from django.contrib import admin
from .models import Feedback
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateTimeRangeFilter

# Register your models here.
class FeedbackAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['rating','review','course','track','created_at']
    list_filter = (('created_at',DateTimeRangeFilter),)
    search_fields = ('rating','review','course','track')


admin.site.register(Feedback, FeedbackAdmin)