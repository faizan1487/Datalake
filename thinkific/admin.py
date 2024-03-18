from django.contrib import admin
from .models import Thinkific_User, Thinkific_Users_Enrollments
from import_export.admin import ImportExportModelAdmin

class ThinkificUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'email', 'full_name','company','created_at']
    search_fields = ('id', 'email', 'first_name', 'last_name')
    
class ThinkificUserEnrollmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'email','course_id','course_name','percentage_completed','user_id','created_at','expiry_date','completed','expired']
    search_fields = ('id', 'email', 'course_name','percentage_completed','created_at','expiry_date','completed','expired','user_id__email')
    


admin.site.register(Thinkific_User, ThinkificUserAdmin)
admin.site.register(Thinkific_Users_Enrollments, ThinkificUserEnrollmentAdmin)
