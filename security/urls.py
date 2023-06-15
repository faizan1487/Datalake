from django.urls import path
from .views import CreateScan

urlpatterns = [
    path("createscan/", CreateScan.as_view(), name="create-scan"),
]