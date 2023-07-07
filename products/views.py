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
        product_id = data.get('id')

        try:
            instance = Alnafi_Product.objects.get(id=product_id)
            serializer = AlNafiMainSiteProductSerializer(instance, data=data)
        except:
            serializer = AlNafiMainSiteProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        queryset = Alnafi_Product.objects.exclude(name__in=['test','test10']).values_list('name', flat=True)
        words_to_remove = ['Wnglish','01_2_7','01_2_4','01_2_6','Brazil','(Italy)',' in english','Bengali','Mandarin',' in','yearly','Annual in english','Half Yearly in english','Quarterly in english','Quarterly','half','Half', 'Monthly', 'Yearly', 'HalfYearly','Annual',' halfyearly','QUARTERLY','annual','Quaterly','TEST','English','english','Urdu','Italian','French','Chinese','Spanish','Arabic','Malay','Indonesian','Hindi','Bangla','Portuguese','Swahili','Russian','Japanese','Persian','Filipino','Turkish','Marathi','Javanese','German','Vietnamese']
        to_not_remove = ['Arabic for Urdu Speakers']
        # return Response(queryset)
    
        query_objects_without_words = []
        for name in queryset:
            for word in words_to_remove:
                if name not in to_not_remove:
                    name = name.replace(word, '')  # Remove the word from the name
            query_objects_without_words.append(name)
        
        
        names_list_without_spaces = [name.rstrip() for name in query_objects_without_words]
        names_list_without_duplicates = list(set(names_list_without_spaces))
        filtered_list = [item for item in names_list_without_duplicates if item != ""]
        
        return Response(filtered_list)