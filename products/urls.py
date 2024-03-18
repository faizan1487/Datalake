from django.urls import path
from .views import AlnafiProduct

urlpatterns = [
    path("alnafiproduct/", AlnafiProduct.as_view(), name='alnafi-product'),
]
