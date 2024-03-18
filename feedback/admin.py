from django.contrib import admin
from .models import Feedback, FeedbackQuestion, FeedbackAnswers
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateTimeRangeFilter

# Register your models here.
class FeedbackAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['user','rating','review','course','track','created_at']
    list_filter = (('created_at',DateTimeRangeFilter),)
    search_fields = ('rating','review','course','track')

class FeedbackQuestionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['chapter_name','course_name']

class FeedbackAnswersAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['user_email','feedback_question_id','created_at']


  
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackAnswers, FeedbackAnswersAdmin)
admin.site.register(FeedbackQuestion, FeedbackQuestionAdmin)