from django.urls import path
from .views import GetFeedbacks

urlpatterns = [
    path("getfeedbacks/", GetFeedbacks.as_view(), name='get-feedbacks'),
]