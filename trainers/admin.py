from django.contrib import admin
from .models import Trainer
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class TrainerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "trainer_name")
    list_filter = ("trainer_name",)


admin.site.register(Trainer, TrainerAdmin)
