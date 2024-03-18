# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Expense
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import IntegrityError


class ExpenseCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)  # Get the names of all user groups
        has_perm = False
        for i in user_groups:
            if i == 'CFO':
                has_perm = True

        if has_perm:
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

                return Response({'id': expense.id,'subject':expense.subject,'amount':expense.amount,'month':expense.month,'currency':expense.currency,'user':expense.user.email,'created_at':expense.created_at}, status=status.HTTP_201_CREATED)

            except KeyError as e:
                return Response({'error': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    
        else:
            return Response({'error': 'You don\'t have permission to enter expense.'}, status=status.HTTP_403_FORBIDDEN)

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
                'user': expense.user.email,  # Assuming user is a ForeignKey in Expense model
                'month': expense.month,  # Extract month from created_at
                'currency': expense.currency,  # Assuming currency is a field in Expense model
            }
            for expense in queryset
        ]

        return Response(expenses_data)
    






class ExpenseUpdateAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, expense_id):
        # Retrieve the expense instance
        try:
            expense = Expense.objects.get(id=expense_id)

            expense_data = {
                    'id': expense.id,
                    'subject': expense.subject,
                    'amount': expense.amount if expense.amount else None,
                    'currency': expense.currency if expense.currency else None,
                    'created_at': expense.created_at if expense.created_at else None,
                    'month': expense.month if expense.month else None,
                    'user': expense.user.email

                }

            return Response(expense_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


    
    def put(self, request, expense_id):
        user_groups = request.user.groups.values_list('name', flat=True)  # Get the names of all user groups

        has_perm = False
        for i in user_groups:
            if i == 'CFO':
                has_perm = True

        if has_perm:
            try:
                expense = Expense.objects.get(id=expense_id)
                data = request.data

                attributes_to_update = [
                    'subject', 'amount','currency', 'created_at', 'month'
                ]

                for attribute in attributes_to_update:
                    if attribute in data:
                        setattr(expense, attribute, data[attribute])

                expense.save()

                expense_data = {
                        'id': expense.id,
                        'subject': expense.subject,
                        'amount': expense.amount if expense.amount else None,
                        'currency': expense.currency if expense.currency else None,
                        'created_at': expense.created_at if expense.created_at else None,
                        'month': expense.month if expense.month else None,
                        'user': expense.user.email

                    }

                return Response(expense_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'You don\'t have permission to update expense.'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, expense_id):
        user_groups = request.user.groups.values_list('name', flat=True)  # Get the names of all user groups

        has_perm = False
        for i in user_groups:
            if i == 'CFO':
                has_perm = True

        if has_perm:
            try:
                expense = Expense.objects.get(pk=expense_id)
                expense.delete()
                return JsonResponse({'message': 'Expense deleted successfully'}, status=200)
            except Expense.DoesNotExist:
                return JsonResponse({'error': 'Expense not found'}, status=404)
            except IntegrityError:
                return JsonResponse({'error': 'IntegrityError occurred while deleting expense'}, status=500)
        else:
            return Response({'error': 'You don\'t have permission to delete expense.'}, status=status.HTTP_403_FORBIDDEN)

