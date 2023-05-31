from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

# Create your views here.
from payment.models import Main_Payment
from payment.serializer import MainPaymentSerializer
from products.models import Alnafi_Product, Main_Product
from trainers.models import Trainer
from user.models import AlNafi_User, Main_User
from user.serializers import MainUserSerializer
from django.db.models import Count, OuterRef, Subquery
from collections import defaultdict
import json

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100     

class GetTrainerStudents(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    required_group = 'Trainer'
    def get(self, request):
        # expiration = self.request.GET.get('expiration_date', None) or None
        # q = self.request.GET.get('q', None) or None
        # source = self.request.GET.get('source', None) or None
        # exact = self.request.GET.get('exact', None) or None
        # export = self.request.GET.get('export', None) or None 
        # plan = self.request.GET.get('plan', None) or None
        # url = request.build_absolute_uri()
        # active = self.request.GET.get('is_active', None) or None
        trainer = self.request.GET.get('trainer', None) or None
        url = request.build_absolute_uri()

        product_name=Alnafi_Product.objects.filter(name='Diploma in Cloud Cyber Security Monthly in Urdu')
        if product_name:
            trainer_students = []
            queryset = AlNafi_Payment.objects.filter(product_name__icontains=product_name[0])
            
            for i in queryset:
                user = AlNafi_User.objects.filter(email=i)
                serializer = AlnafiUserSerializer(user[0])
                trainer_students.append(serializer.data)
                
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(trainer_students, request)
            return paginator.get_paginated_response(paginated_queryset)
            # print(serializer)
            # print(serializer.data)
            # return Response(trainer_students)


class TrainersData(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Sales', 'Admin']
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        export = self.request.GET.get('export', None) or None
        # create a datetime object for 24 hours ago
        url = request.build_absolute_uri()  
        
      
        # payments = Main_Payment.objects.filter(product__product_name__icontains='Python Automation - Tools and handson')
        # print(payments)
        # payments = payments.exclude(amount__in=[0,0.1,1,2,0.01,1.0,2.0,3.0,4.0,5.0,5.0,6.0,7.0,8.0,9.0,10.0,10])
        # distinct_users = payments.order_by('user').values('user').distinct()


        trainers = Trainer.objects.annotate(total_users=Count('products__product_payments__user', distinct=True)).values('trainer_name', 'products__product_name', 'products__product_payments__user__email','products__product_payments__user__username')

        # Create a dictionary to store the grouped data
        grouped_data = defaultdict(lambda: defaultdict(list))

        # Iterate over the queryset and group the data
        for trainer in trainers:
            trainer_name = trainer['trainer_name']
            product_name = trainer['products__product_name']
            user_email = trainer['products__product_payments__user__username' if 'products__product_payments__user__email' == None else 'products__product_payments__user__email']
            grouped_data[trainer_name][product_name].append(user_email)

        # print(grouped_data)

        # Convert the grouped data to a list of dictionaries
        result = []
        for trainer_name, products in grouped_data.items():
            # print("trainer_namee",trainer_name)
            # print("products",products)
            for product_name, users in products.items():
                result.append({
                    'trainer_name': trainer_name,
                    'product_name': product_name,
                    # 'users': users,
                    'user_count': len(users)-1 if users[0] == None else len(users)
                })
                # print("users",len(users))

        # print(result[-1])
        # payments = payments.filter(user__id__in=Subquery(distinct_users)).values('product__id', 'product__product_name').annotate(total_payments=Count('id'))
        return Response(result)


        