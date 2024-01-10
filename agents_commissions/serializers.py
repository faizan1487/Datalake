from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField, ValidationError
from .models import Daily_lead

#For AlNafi (MainSite) Payments:
class DailyLeadSerializer(ModelSerializer):
    class Meta:
        model = Daily_lead
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.status = validated_data.get('status', instance.status)
        instance.product = validated_data.get('product', instance.product)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.lead_creator = validated_data.get('lead_creator', instance.lead_creator)
        instance.al_baseer_verify = validated_data.get('al_baseer_verify', instance.al_baseer_verify)
        instance.crm_verify = validated_data.get('crm_verify', instance.crm_verify)

        instance.save()
        return instance