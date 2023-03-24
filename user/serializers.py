from rest_framework import serializers
from .models import AlnafiUser
from .models import IslamicAcademyUser


# For Main Site Al-Nafi User Table:
class AlnafiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlnafiUser
        fields = '__all__'


# For Islamic Academy Users:

class IslamicAcademyUserSerializer(serializers.ModelSerializer):
    address = serializers.JSONField()

    class Meta:
        model = IslamicAcademyUser
        fields = '__all__'