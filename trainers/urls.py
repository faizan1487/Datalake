from django.urls import path
from .views import (GetTrainerStudents,TrainersData)

urlpatterns = [
    path("trainertudents/", GetTrainerStudents.as_view(), name='trainer-students'),
    path("trainersdata/", TrainersData.as_view(), name='trainers-data'),
    
]