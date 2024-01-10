from django.urls import path
from .views import DailyLead

urlpatterns = [
    path('daily-lead/', DailyLead.as_view()),
]