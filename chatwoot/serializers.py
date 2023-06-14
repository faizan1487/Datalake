from rest_framework import serializers
from .models import ChatwoorUser
from rest_framework.serializers import ModelSerializer

class ChatwootUserSerializer(ModelSerializer):
    class Meta:
        model = ChatwoorUser
        fields = '__all__'
