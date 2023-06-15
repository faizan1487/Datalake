from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ScanSerializer
from .models import Scan
from user.models import User
# Create your views here.



class CreateScan(APIView):
    def get(self,request):
        scans = Scan.objects.values('id', 'scan_type', 'scan_date','severity','remediation',
                                    'assigned_to','scan_progress','testing_method','target','http_or_https',
                                    'application_type','findings_and_recommendations','file_upload','poc')
        # serializer = GetAlnafipaymentSerializer(alnafi_payment, many=True)
        return Response(scans)
    
    def post(self, request):
        data = request.data
        # print(data)
        # print(data['assigned_to'])
        team_member = User.objects.get(email=data['assigned_to'])
        # print(team_member.id)
        data['assigned_to'] = team_member.id
        serializer = ScanSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
