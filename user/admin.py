from django.contrib import admin
from .models import AlNafi_User
from .models import IslamicAcademy_User
from import_export.admin import ImportExportModelAdmin


# Register your models here

# For MainSite Users:
class AlnafiUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'created_at', 'address', 'country', 'language', 'verification_code', 'isAffiliate', 'how_did_you_hear_about_us', 'affiliate_code', 'isMentor')
    search_fields = ('id', 'username', 'email', 'phone')
    list_filter = ('created_at', 'isAffiliate', 'isMentor', 'language', 'country')

admin.site.register(AlNafi_User, AlnafiUserAdmin)


# For Islamic Academy Users:
class IslamicAcademyUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','is_paying_customer','username','email','first_name','last_name','created_at','modified_at','role','phone','address']
    search_fields = ('id', 'email', 'username', 'phone')
    list_filter = ('created_at',"is_paying_customer", "role")

admin.site.register(IslamicAcademy_User, IslamicAcademyUserAdmin)
 