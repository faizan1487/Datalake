from django.contrib import admin
from secrets_api.models import LastSecretApiUsing, AllSecretsApi, SupportLastSecretApiUsing, SupportAllSecretsApi, ExamAllSecretsApi, ExamLastSecretApiUsing
from albaseer.settings import DEBUG
from import_export.admin import ImportExportModelAdmin,ExportActionMixin

class LastSecretApiUsingAdmin(ImportExportModelAdmin,ExportActionMixin,admin.ModelAdmin):
    list_display = ['user_name','turn_number','api_key','secret_key']
    search_fields = ['user_name','turn_number','api_key','secret_key']
    list_filter = ['turn_number']
    # if not DEBUG:
    # readonly_fields = list_display
    
admin.site.register(LastSecretApiUsing,LastSecretApiUsingAdmin)

class SupportLastSecretApiUsingAdmin(ImportExportModelAdmin,ExportActionMixin,admin.ModelAdmin):
    list_display = ['user_name','turn_number','api_key','secret_key']
    search_fields = ['user_name','turn_number','api_key','secret_key']
    list_filter = ['turn_number']

admin.site.register(SupportLastSecretApiUsing,SupportLastSecretApiUsingAdmin)

class AllSecretsApiAdmin(ImportExportModelAdmin,ExportActionMixin,admin.ModelAdmin):
    list_display = ['user_name','turn_number','api_key','secret_key']
    search_fields = ['user_name','api_key','secret_key']
    list_filter = ['turn_number']
    # if not DEBUG:
    # readonly_fields = list_display
        
admin.site.register(AllSecretsApi,AllSecretsApiAdmin)


class SupportAllSecretsApiAdmin(ImportExportModelAdmin,ExportActionMixin,admin.ModelAdmin):
    list_display = ['user_name','turn_number','api_key','secret_key']
    search_fields = ['user_name','api_key','secret_key']
    list_filter = ['turn_number']
    # if not DEBUG:
    # readonly_fields = list_display
        
admin.site.register(SupportAllSecretsApi,SupportAllSecretsApiAdmin)
        
class ExamAllSecretsApiAdmin(ImportExportModelAdmin,ExportActionMixin,admin.ModelAdmin):
    list_display = ['user_name','turn_number','api_key','secret_key']
    search_fields = ['user_name','api_key','secret_key']
    list_filter = ['turn_number']
    # if not DEBUG:
    # readonly_fields = list_display
        
admin.site.register(ExamAllSecretsApi,ExamAllSecretsApiAdmin)

class ExamLastSecretApiUsingAdmin(ImportExportModelAdmin,ExportActionMixin,admin.ModelAdmin):
    list_display = ['user_name','turn_number','api_key','secret_key']
    search_fields = ['user_name','api_key','secret_key']
    list_filter = ['turn_number']
    # if not DEBUG:
    # readonly_fields = list_display
        
admin.site.register(ExamLastSecretApiUsing, ExamLastSecretApiUsingAdmin)
