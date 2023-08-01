from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from .models  import AffiliateUser, AffiliateUniqueClick, AffiliateLead



class AffiliateSerializer(ModelSerializer):
    class Meta:
        model = AffiliateUser
        fields = '__all__'
        
    def update(self, instance, validated_data):
        # instance.source_id = validated_data.get('source_id', instance.source_id)
        # instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.first_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.country = validated_data.get('country', instance.country)
        # instance.language = validated_data.get('language', instance.language)
        # instance.referral_code = validated_data.get('referral_code', instance.referral_code)
        # instance.category_code = validated_data.get('category_code', instance.category_code)
        # instance.accept_aggrement = validated_data.get('accept_aggrement', instance.accept_aggrement)

        instance.save()
        return instance
    
class AffiliateLeadSerializer(ModelSerializer):
    class Meta:
        model = AffiliateLead
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.affiliate = validated_data.get('affiliate', instance.affiliate)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.address = validated_data.get('address', instance.address)
        instance.country = validated_data.get('country', instance.country)

        instance.save()
        return instance
    


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