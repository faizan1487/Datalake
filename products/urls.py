from django.urls import path
from .models import AlnafiProduct
from . import views

urlpatterns = [
    path('', AlnafiProduct.index, name='index'),
]
