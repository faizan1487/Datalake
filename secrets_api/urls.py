from django.urls import path
from .views import GetData

urlpatterns = [
    path('get-data/',GetData.as_view())
]