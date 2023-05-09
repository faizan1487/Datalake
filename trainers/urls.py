from django.urls import path
from .views import (GetTrainerStudents)

urlpatterns = [
    path("trainertudents/", GetTrainerStudents.as_view(), name='trainer-students'),
]