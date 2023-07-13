from rest_framework import serializers
from .models import ChatwoorUser
from rest_framework.serializers import ModelSerializer

class ChatwootUserSerializer(ModelSerializer):
    class Meta:
        model = ChatwoorUser
        fields = '__all__'


    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)

        instance.save()
        return instance
