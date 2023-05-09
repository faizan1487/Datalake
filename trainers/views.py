from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

# Create your views here.
from payment.models import AlNafi_Payment
from payment.serializer import AlNafiPaymentSerializer
from products.models import Alnafi_Product
from user.models import AlNafi_User
from user.serializers import AlnafiUserSerializer

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