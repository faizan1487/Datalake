from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("payments/",include('payment.urls')),
    path("",include('user.urls')),
]
