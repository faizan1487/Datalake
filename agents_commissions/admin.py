from django.contrib import admin
from rest_framework.serializers import ModelSerializer
from .models import Daily_lead, Daily_Sales_Support
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

# Register your models here.

class DailyLeadAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('id','email','phone','status','product','plan','amount','lead_creator','support','manager_approval','manager_approval_crm', 'veriification_cfo','created_at')
    search_fields = ('email','phone','status','product','amount','lead_creator','created_at','plan')
    list_filter = ('status','product','lead_creator','created_at','plan')


admin.site.register(Daily_lead, DailyLeadAdmin)
class DailySalesSupportAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('id','email','phone','status','product','plan','amount','lead_creator','manager_approval','manager_approval_crm', 'veriification_cfo','created_at')
    search_fields = ('email','phone','status','product','amount','lead_creator','created_at','plan')
    list_filter = ('status','product','lead_creator','created_at','plan')


admin.site.register(Daily_Sales_Support, DailySalesSupportAdmin)