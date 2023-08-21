from django.contrib import admin
from .models import Trainer
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class TrainerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "trainer_name","email")
    list_filter = ("trainer_name","email")
    filter_horizontal =  (
        'products',
    )


admin.site.register(Trainer, TrainerAdmin)
