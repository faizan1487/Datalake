from django.urls import path
from .views import GetUserDetails

urlpatterns = [
    path('users/', GetUserDetails.as_view(), name='user-list'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]
