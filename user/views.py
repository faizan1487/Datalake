from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import AlnafiUser, IslamicAcademyUser
from .serializers import UserSerializer
# Create your views here.

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100   
# class GetUserDetails(APIView):
#     def post(self, request):
#         email = request.data['email']
#         queryset = User.objects.filter(email=email)
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)
class SearchUsers(APIView):
    def get(self, request):
        query = self.request.GET.get('q')
        source = self.request.GET.get('source')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
           
        if source=='easypaisa':
            easypaisa_obj = easypaisa_pay(query, start_date, end_date, source)
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(easypaisa_obj, request)
            easypaisa_serializer = Easypaisa_PaymentsSerializer(paginated_queryset,many=True)
            return paginator.get_paginated_response(easypaisa_serializer.data)
        elif source=='stripe':
            stripe_obj = stripe_pay(query, start_date, end_date, source)
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(stripe_obj, request)
            stripe_serializer = PaymentSerializer(paginated_queryset,many=True)
            return paginator.get_paginated_response(stripe_serializer.data)
        elif source == 'ubl':
            ubl_obj = ubl_pay(query, start_date, end_date, source)
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(ubl_obj, request)
            ubl_serializer = Ubl_Ipg_PaymentsSerializer(paginated_queryset,many=True)
            return paginator.get_paginated_response(ubl_serializer.data)
        else:
            easypaisa_obj = easypaisa_pay(query, start_date, end_date, source)
            stripe_obj = stripe_pay(query, start_date, end_date, source)
            ubl_obj = ubl_pay(query, start_date, end_date, source) 
            
            queryset = list(easypaisa_obj) + list(stripe_obj) + list(ubl_obj)
            
            serializer_dict = {
                Payment: PaymentSerializer,
                Easypaisa_Payment: Easypaisa_PaymentsSerializer,
                UBL_IPG_Payment: Ubl_Ipg_PaymentsSerializer
            }
            
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = []
            for obj in paginated_queryset:
                serializer_class = serializer_dict.get(obj.__class__)
                serializer.append(serializer_class(obj).data)
            
            return paginator.get_paginated_response(serializer)        