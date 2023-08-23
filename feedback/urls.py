from django.urls import path
from .views import GetFeedbacks, GetFeedbackAnswers,GetCoursesNames, GetCoursesChapters

urlpatterns = [
    path("getfeedbacks/", GetFeedbacks.as_view(), name='get-feedbacks'),
    path("getfeedbacksasnwers/", GetFeedbackAnswers.as_view(), name='get-feedbacks-answers'),
    path("getcoursesnames/", GetCoursesNames.as_view(), name='get-courses-names'),
    path("getchaptersnames/", GetCoursesChapters.as_view(), name='get-chapters-names'),
]