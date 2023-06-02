from django.urls import path
from .views import (TrainersData,AnalyticsTrainers)

urlpatterns = [
    path("trainersdata/", TrainersData.as_view(), name='trainers-data'),
    path("analytictrainers/", AnalyticsTrainers.as_view(), name='analytics-trainers')
]