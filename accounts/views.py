# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Expense
from rest_framework.permissions import IsAuthenticated


class ExpenseCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            subject = data['subject']
            amount = data['amount']
            month = data['month']
            currency = data['currency']

            # Check if an expense with the same details already exists
            existing_expense = Expense.objects.filter(
                subject=subject,
                amount=amount,
                user_id=request.user.id,
                month=month,
                currency=currency
            ).first()

            if existing_expense:
                return Response({'error': 'Expense with the same details already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Create Expense object
            expense = Expense.objects.create(
                subject=subject,
                amount=amount,
                user_id=request.user.id,
                month=month,
                currency=currency
            )

            return Response({'id': expense.id}, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({'error': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    

    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Get parameters from the request
        month = request.GET.get('month')
        subject = request.GET.get('subject')
        amount = request.GET.get('amount')
        created_at = request.GET.get('created_at')


        # Start with all expenses
        queryset = Expense.objects.all()

        # Filter based on provided parameters
        if month:
            queryset = queryset.filter(month=month)
        if subject:
            queryset = queryset.filter(subject__icontains=subject)
        if amount:
            queryset = queryset.filter(amount=amount)
        if created_at:
            queryset = queryset.filter(created_at__date=created_at)

        # Create a list of dictionaries from the queryset
        expenses_data = [
            {
                'id': expense.id,
                'subject': expense.subject,
                'amount': expense.amount,
                'created_at': expense.created_at,
                'user': expense.user.id,  # Assuming user is a ForeignKey in Expense model
                'month': expense.month,  # Extract month from created_at
                'currency': expense.currency,  # Assuming currency is a field in Expense model
            }
            for expense in queryset
        ]

        return Response(expenses_data)