# your_app/urls.py
from django.urls import path
from .views import ExpenseCreateAPIView,ExpenseUpdateAPIView

urlpatterns = [
    path('expenses/create/', ExpenseCreateAPIView.as_view(), name='expense-create'),
    path('expenses/update/<int:expense_id>/', ExpenseUpdateAPIView.as_view(), name='update_expense'),

]
