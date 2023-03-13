from rest_framework import serializers
from .models import User
from .models import IslamicAcademyUser


# For Main Site Al-Nafi User Table:
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# For Islamic Academy Users:

class IslamicAcademyUserSerializer(serializers.ModelSerializer):
    address = serializers.JSONField()

    class Meta:
        model = IslamicAcademyUser
        fields = '__all__'