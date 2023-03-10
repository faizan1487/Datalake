from django.contrib import admin
from .models import User
from .models import IslamicAcademyUser
from import_export.admin import ImportExportModelAdmin


# Register your models here

# For MainSite Users:
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'created_at')
    per_page = 500
    search_fields = ('email', 'phone')
    list_filter = ('created_at',)

admin.site.register(User, UserAdmin)


# For Islamic Academy Users:
class IslamicAcademyUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','is_paying_customer','username','email','first_name','last_name','date_created','date_modified','role','phone','address']
    per_page = 500
    search_fields = ('id', 'email', 'username')
    list_filter = ('date_created',"is_paying_customer", "role")

admin.site.register(IslamicAcademyUser, IslamicAcademyUserAdmin)

