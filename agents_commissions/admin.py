from django.contrib import admin
from rest_framework.serializers import ModelSerializer
from .models import Daily_lead, Daily_Sales_Support, Deleted_Daily_lead, Deleted_Daily_Sales_Support
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

# Register your models here.

class DailyLeadAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('id','email','phone','status','product','plan','amount','lead_creator','support','manager_approval','manager_approval_crm', 'veriification_cfo','is_exam_fee','renewal','created_at')
    search_fields = ('id','email','phone','status','product','amount','lead_creator','created_at','plan')
    list_filter = ('id','status','product','lead_creator','created_at','plan')


admin.site.register(Daily_lead, DailyLeadAdmin)


class Deleted_Daily_leadAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('crm_id','email','phone','status','product','plan','amount','lead_creator','support','manager_approval','manager_approval_crm', 'veriification_cfo','is_exam_fee','renewal','created_at')
    search_fields = ('email','phone','status','product','amount','lead_creator','created_at','plan')
    list_filter = ('status','product','lead_creator','created_at','plan')


admin.site.register(Deleted_Daily_lead, Deleted_Daily_leadAdmin)
class DailySalesSupportAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('id','email','phone','status','product','plan','amount','lead_creator','manager_approval','manager_approval_crm', 'veriification_cfo','created_at')
    search_fields = ('email','phone','status','product','amount','lead_creator','created_at','plan')
    list_filter = ('status','product','lead_creator','created_at','plan')


admin.site.register(Daily_Sales_Support, DailySalesSupportAdmin)

class Deleted_daily_supportAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('crm_id','email','phone','status','product','plan','amount','lead_creator','manager_approval','manager_approval_crm', 'veriification_cfo','created_at')
    search_fields = ('email','phone','status','product','amount','lead_creator','created_at','plan')
    list_filter = ('status','product','lead_creator','created_at','plan')


admin.site.register(Deleted_Daily_Sales_Support, Deleted_daily_supportAdmin)