from django.shortcuts import render
from .models import Payment, Easypaisa_Payment, UBL_IPG_Payment
from .serializer import PaymentSerializer, Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer
from .services import easypaisa_payment, stripe_payment, ubl_payment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

# Create your views here.

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    
class GetAllUserDetails(APIView):

    def get(self,request):   
        easypaisa_obj = Easypaisa_Payment.objects.all()
        stripe_obj = Payment.objects.all()
        ubl_obj = UBL_IPG_Payment.objects.all()
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


class GetUserDetails(APIView):

    def post(self,request):
        email = request.data['email']
        
        easypaisa_obj = easypaisa_payment(email)
        easypaisa_serializer = Easypaisa_PaymentsSerializer(easypaisa_obj,many=True)
        
        stripe_obj = stripe_payment(email)
        stripe_serializer = PaymentSerializer(stripe_obj,many=True)
        
        ubl_obj = ubl_payment(email)
        ubl_serializer = Ubl_Ipg_PaymentsSerializer(ubl_obj,many=True)
        
        data = {
            'easypaisa': easypaisa_serializer.data,
            'stripe': stripe_serializer.data,
            'ubl': ubl_serializer.data
        }
        
        return Response(data)

    
class GetEasyPaisaUserDetails(APIView):

    def get(self,request):
        queryset = Easypaisa_Payment.objects.all()
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serialized_data = Easypaisa_PaymentsSerializer(paginated_queryset,many=True)
        return paginator.get_paginated_response(serialized_data.data)
    
        
class GetStripeUserDetails(APIView):

    def get(self,request):
        queryset = Payment.objects.all()
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serialized_data = PaymentSerializer(paginated_queryset,many=True)
        return paginator.get_paginated_response(serialized_data.data)
        
        
class GetUblUserDetails(APIView):

    def get(self,request):
        queryset = UBL_IPG_Payment.objects.all()
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serialized_data = Ubl_Ipg_PaymentsSerializer(paginated_queryset,many=True)
        return paginator.get_paginated_response(serialized_data.data)
      
    
class SearchUser(APIView):
    def get(self, request):
        query = self.request.GET.get('q')
        print(query)
        queryset = Payment.objects.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        )
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serialized_data = PaymentSerializer(paginated_queryset,many=True)
        return paginator.get_paginated_response(serialized_data.data)