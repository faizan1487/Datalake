from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from .models  import Newsletter



class NewsletterSerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'
        
    def update(self, instance, validated_data):
      instance.first_name = validated_data.get('first_name', instance.first_name)
      instance.phone = validated_data.get('phone', instance.phone)
      # instance.email = validated_data.get('email', instance.email)      

      instance.save()
      return instance