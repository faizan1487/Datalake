from django.urls import path
from .views import DailyLead, DailySalesSupport, ResaveLeadsAPIView

urlpatterns = [
    path('daily-lead/', DailyLead.as_view()),
    path("daily_support/", DailySalesSupport.as_view()),
    path("resave/", ResaveLeadsAPIView.as_view()),
]