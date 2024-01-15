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
        instance.renewal = validated_data.get('renewal', instance.renewal)
        instance.lead_creator = validated_data.get('lead_creator', instance.lead_creator)
        instance.manager_approval = validated_data.get('manager_approval', instance.manager_approval)
        instance.manager_approval_crm = validated_data.get('manager_approval_crm', instance.manager_approval_crm)
        instance.veriification_cfo = validated_data.get('veriification_cfo', instance.veriification_cfo)
        instance.plan = validated_data.get('plan', instance.plan)
        instance.source = validated_data.get('source', instance.source)

        instance.save()
        return instance
