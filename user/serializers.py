from rest_framework import serializers
from .models import AlNafi_User
from .models import IslamicAcademy_User


# For Main Site Al-Nafi User Table:
class AlnafiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlNafi_User
        fields = '__all__'


# For Islamic Academy Users:
class IslamicAcademyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IslamicAcademy_User
        fields = '__all__'