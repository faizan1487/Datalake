from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from .models  import Newsletter



class NewsletterSerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'
        
    def create(self, validated_data):
        # Get the ID of the object to update, if it exists
        my_email = validated_data.get('email')
        
        # If an ID was provided, try to get the existing object
        if my_email:
            try:
                obj = Newsletter.objects.get(email=my_email)
            except Newsletter.DoesNotExist:
                obj = None
        else:
            obj = None
        
        # If the object exists, update its fields with the validated data
        if obj:
            for key, value in validated_data.items():
                setattr(obj, key, value)
            obj.save()
        else:
            obj = Newsletter.objects.create(**validated_data)
        
        return obj