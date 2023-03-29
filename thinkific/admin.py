from django.contrib import admin
from .models import Thinkific_User
from import_export.admin import ImportExportModelAdmin

class ThinkificUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = []
    search_fields = ('id', 'email', 'first_name', 'last_name')
    
admin.site.register(Thinkific_User, ThinkificUserAdmin)
