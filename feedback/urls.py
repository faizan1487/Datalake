from django.urls import path
from .views import GetFeedbacks, GetFeedbackAnswers,GetCoursesNames, GetCoursesChapters, GetFeedbackProgress

urlpatterns = [
    path("getfeedbacks/", GetFeedbacks.as_view(), name='get-feedbacks'),
    path("getfeedbacksasnwers/", GetFeedbackAnswers.as_view(), name='get-feedbacks-answers'),
    path("getfeedbackprogress/", GetFeedbackProgress.as_view(), name='get-feedbacks-progress'),
    path("getcoursesnames/", GetCoursesNames.as_view(), name='get-courses-names'),
    path("getchaptersnames/", GetCoursesChapters.as_view(), name='get-chapters-names'),
]