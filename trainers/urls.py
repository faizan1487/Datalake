from django.urls import path
from .views import (TrainersData,AnalyticsTrainers,TrainersName,TrainerProducts)

urlpatterns = [
    path("trainersdata/", TrainersData.as_view(), name='trainers-data'),
    path("analytictrainers/", AnalyticsTrainers.as_view(), name='analytics-trainers'),
    path("trainersname/", TrainersName.as_view(), name='trainers-names'),
    path("trainerproducts/", TrainerProducts.as_view(), name='trainer-products')
]