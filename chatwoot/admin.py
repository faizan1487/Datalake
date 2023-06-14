from django.contrib import admin
from .models import ChatwoorUser
from import_export.admin import ImportExportModelAdmin

class ChatwootUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name']
    search_fields = ('id', 'email', 'first_name')


admin.site.register(ChatwoorUser, ChatwootUserAdmin)