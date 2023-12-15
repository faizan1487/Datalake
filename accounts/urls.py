# your_app/urls.py
from django.urls import path
from .views import ExpenseCreateAPIView

urlpatterns = [
    path('expenses/create/', ExpenseCreateAPIView.as_view(), name='expense-create'),
]
