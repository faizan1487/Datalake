
from django.urls import path
from .views import GetUserDetails 
urlpatterns = [
    path("",GetUserDetails.as_view(),name='get_users_details')

]
