from django.contrib import admin
from rest_framework.serializers import ModelSerializer
from .models import Daily_lead
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

# Register your models here.

class DailyLeadAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('email','phone','status','product','amount','lead_creator','al_baseer_verify','crm_verify','created_at')
    search_fields = ('email','phone','status','product','amount','lead_creator','created_at')
    list_filter = ('status','product','lead_creator','created_at')


admin.site.register(Daily_lead, DailyLeadAdmin)