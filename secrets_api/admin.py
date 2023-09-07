from django.contrib import admin
from secrets_api.models import LastSecretApiUsing, AllSecretsApi
from albaseer.settings import DEBUG

class LastSecretApiUsingAdmin(admin.ModelAdmin):
    list_display = ['user_name','turn_number','api_key','secret_key']
    search_fields = ['user_name','turn_number','api_key','secret_key']
    list_filter = ['turn_number']
    if not DEBUG:
        readonly_fields = list_display
    

admin.site.register(LastSecretApiUsing,LastSecretApiUsingAdmin)

class AllSecretsApiAdmin(admin.ModelAdmin):
    list_display = ['user_name','turn_number','api_key','secret_key']
    search_fields = ['user_name','api_key','secret_key']
    list_filter = ['turn_number']
    if not DEBUG:
        readonly_fields = list_display
        
admin.site.register(AllSecretsApi,AllSecretsApiAdmin)