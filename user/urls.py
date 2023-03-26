from django.urls import path
from .views import GetUserDetails, Import_csv

urlpatterns = [
    path('users/', GetUserDetails.as_view(), name='user-list'),
    path('import-csv/', Import_csv.as_view(), name='import_csv'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]
