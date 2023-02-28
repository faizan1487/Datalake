from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'created_at')
    per_page = 500
    search_fields = ('email', 'phone')

admin.site.register(User, UserAdmin)
