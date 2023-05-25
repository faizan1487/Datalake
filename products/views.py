from django.shortcuts import render
from rest_framework.views import APIView
from .models import Alnafi_Product
from .serializers import AlNafiMainSiteProductSerializer
from rest_framework import status
from rest_framework.response import Response
# Create your views here.
class AlnafiProduct(APIView):
    def post(self, request):
        data = request.data
        serializer = AlNafiMainSiteProductSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        data = Alnafi_Product.objects.exclude(name__in=['test','test10']).values_list('name', flat=True)
        words_to_remove = ['Quarterly', 'Monthly', 'Yearly', 'Half Yearly','Annual',' Half yearly','QUARTERLY','annual','Quaterly','TEST']

        query_objects_without_words = [name for name in data if not any(word in name for word in words_to_remove)]
        return Response(query_objects_without_words)