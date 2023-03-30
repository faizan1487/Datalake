from rest_framework import serializers
from .models import Thinkific_User
from rest_framework.serializers import ModelSerializer

class ThinkificUserSerializer(ModelSerializer):
    print("thinkific serailizer")
    class Meta:
        model = Thinkific_User
        fields = '__all__'