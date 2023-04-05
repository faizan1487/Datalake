from django.contrib import admin
from .models import AlNafi_User
from user.models import IslamicAcademy_User, User
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


class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'name','is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name',)}),
      ('Permissions', {'fields': ('is_admin',)}),
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
