from django.urls import path
from .views import GetUserDetails
from django.http import HttpResponse

urlpatterns = [
    path("", lambda req: HttpResponse(status=200)),
    path('users/', GetUserDetails.as_view(), name='user-list'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]
