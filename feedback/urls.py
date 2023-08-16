from django.urls import path
from .views import GetFeedbacks, GetFeedbackAnswers

urlpatterns = [
    path("getfeedbacks/", GetFeedbacks.as_view(), name='get-feedbacks'),
    path("getfeedbacksasnwers/", GetFeedbackAnswers.as_view(), name='get-feedbacks-answers'),
]