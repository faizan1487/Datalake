from django.contrib import admin
from .models import Contacts, Inbox, Agent, Conversation
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateTimeRangeFilter

class ConversationsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['contact', 'channel','agent','id','inbox','created_at']
    list_filter = (('created_at',DateTimeRangeFilter),)
    search_fields = ('channel','id','created_at')



class ContactsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name','created_at','inbox']
    search_fields = ('id', 'email', 'first_name')



class InboxAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'channel_type']
    search_fields = ('id', 'name', 'channel_type')



class AgentsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['email', 'name','available_name','role']
    search_fields = ('email', 'name','available_name','role')


admin.site.register(Agent, AgentsAdmin)
admin.site.register(Inbox, InboxAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Conversation, ConversationsAdmin)