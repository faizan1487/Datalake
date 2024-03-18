from django.urls import path
from .views import DailyLead, DailySalesSupport, ResaveLeadsAPIView, MatchingId,UpdateDailyLead

urlpatterns = [
    path('daily-lead/', DailyLead.as_view()),
    path("daily_support/", DailySalesSupport.as_view()),
    path("resave/", ResaveLeadsAPIView.as_view()),
    path("matching_data/", MatchingId.as_view(),),
    path("update_data/", UpdateDailyLead.as_view(),)
]