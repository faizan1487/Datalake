from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class GetUserDetails(APIView):
    def post(self, request):
        email = request.data['email']
        queryset = User.objects.filter(email=email)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
