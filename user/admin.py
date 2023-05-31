from django.contrib import admin
from .models import AlNafi_User
from .models import Main_User
from user.models import IslamicAcademy_User, User, NavbarLink
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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


#FOR MERGE USERS TABLES MAIN_USER:
class Main_UserAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","username", "first_name", "last_name", "email", "source", "phone", "address", "country", "language", "created_at", "modified_at", "verification_code", "isAffiliate", "how_did_you_hear_about_us", "affiliate_code", "isMentor", "is_paying_customer", "role"]
    search_fields = ("username", "first_name", "last_name", "email", "source", "phone", "address", "country", "language", "created_at", "modified_at", "verification_code", "isAffiliate", "affiliate_code", "isMentor", "is_paying_customer", "role")
    list_filter = ("source", "country", "language", "created_at", "modified_at", "verification_code", "isMentor", "is_paying_customer", "role")

admin.site.register(Main_User, Main_UserAdmin)

class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'name','department','is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name','phone','department',)}),
      ('Permissions', {'fields': ('is_admin','groups','user_permissions')}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name', 'password1', 'password2'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)


class NavbarLinkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'path')

admin.site.register(NavbarLink,NavbarLinkAdmin)   
