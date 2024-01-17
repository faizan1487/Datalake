from django.urls import path
from .views import DailyLead, DailySalesSupport

urlpatterns = [
    path('daily-lead/', DailyLead.as_view()),
    path("daily_support/", DailySalesSupport.as_view()),
]