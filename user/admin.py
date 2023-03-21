from django.contrib import admin
from .models import AlnafiUser
from .models import IslamicAcademyUser
from import_export.admin import ImportExportModelAdmin


# Register your models here

# For MainSite Users:
class AlnafiUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'created_at', 'address', 'country', 'language', 'verification_code', 'isAffiliate', 'how_did_you_hear_about_us', 'affiliate_code', 'isMentor')
    per_page = 500
    search_fields = ('id', 'username', 'email', 'phone')
    list_filter = ('created_at', 'isAffiliate', 'isMentor', 'language', 'country')

admin.site.register(AlnafiUser, AlnafiUserAdmin)


# For Islamic Academy Users:
class IslamicAcademyUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','is_paying_customer','username','email','first_name','last_name','date_created','date_modified','role','phone','address']
    per_page = 500
    search_fields = ('id', 'email', 'username', 'phone')
    list_filter = ('date_created',"is_paying_customer", "role")

admin.site.register(IslamicAcademyUser, IslamicAcademyUserAdmin)
 