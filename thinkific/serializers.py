from rest_framework import serializers
from .models import Thinkific_User, Thinkific_Users_Enrollments
from rest_framework.serializers import ModelSerializer

class ThinkificUserSerializer(ModelSerializer):
    class Meta:
        model = Thinkific_User
        fields = '__all__'
        
        
class ThinkificUserEnrollmentSerializer(ModelSerializer):
    class Meta:
        model = Thinkific_Users_Enrollments
        fields = '__all__'