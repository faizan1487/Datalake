from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from .models  import AffiliateUser, AffiliateUniqueClick



class AffiliateSerializer(ModelSerializer):
    class Meta:
        model = AffiliateUser
        fields = '__all__'
        
    def create(self, validated_data):
        # Get the ID of the object to update, if it exists
        my_email = validated_data.get('email')
        
        # If an ID was provided, try to get the existing object
        if my_email:
            try:
                obj = AffiliateUser.objects.get(email=my_email)
            except AffiliateUser.DoesNotExist:
                obj = None
        else:
            obj = None
        
        # If the object exists, update its fields with the validated data
        if obj:
            for key, value in validated_data.items():
                setattr(obj, key, value)
            obj.save()
        else:
            obj = AffiliateUser.objects.create(**validated_data)
        
        return obj
    


class AffiliateClickSerializer(ModelSerializer):
    class Meta:
        model = AffiliateUniqueClick
        fields = '__all__'
        
    def create(self, validated_data):
        # Get the ID of the object to update, if it exists
        affiliate_id = validated_data.get('affiliate_id')
        
        # If an ID was provided, try to get the existing object
        if affiliate_id:
            try:
                obj = AffiliateUniqueClick.objects.get(affiliate_id=affiliate_id)
            except AffiliateUniqueClick.DoesNotExist:
                obj = None
        else:
            obj = None
        
        # If the object exists, update its fields with the validated data
        if obj:
            for key, value in validated_data.items():
                setattr(obj, key, value)
            obj.save()
        else:
            obj = AffiliateUniqueClick.objects.create(**validated_data)
        
        return obj