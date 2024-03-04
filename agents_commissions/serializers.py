from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField, ValidationError
from .models import Daily_lead, Daily_Sales_Support

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
        instance.is_exam_fee = validated_data.get('is_exam_fee', instance.is_exam_fee)
        instance.lead_creator = validated_data.get('lead_creator', instance.lead_creator)
        instance.manager_approval = validated_data.get('manager_approval', instance.manager_approval)
        instance.manager_approval_crm = validated_data.get('manager_approval_crm', instance.manager_approval_crm)
        instance.veriification_cfo = validated_data.get('veriification_cfo', instance.veriification_cfo)
        instance.plan = validated_data.get('plan', instance.plan)
        instance.source = validated_data.get('source', instance.source)
        instance.completely_verified =  validated_data.get("completely_verified", instance.completely_verified)
        instance.paid =  validated_data.get("paid", instance.paid)
        instance.support = validated_data.get('support', instance.support)
        instance.is_comission = validated_data.get("is_comission", instance.is_comission)

        instance.save()
        return instance
class DailySalesSupportSerializer(ModelSerializer):
    class Meta:
        model = Daily_Sales_Support
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.status = validated_data.get('status', instance.status)
        instance.product = validated_data.get('product', instance.product)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.is_exam_fee = validated_data.get('is_exam_fee', instance.is_exam_fee)
        instance.lead_creator = validated_data.get('lead_creator', instance.lead_creator)
        instance.manager_approval = validated_data.get('manager_approval', instance.manager_approval)
        instance.manager_approval_crm = validated_data.get('manager_approval_crm', instance.manager_approval_crm)
        instance.veriification_cfo = validated_data.get('veriification_cfo', instance.veriification_cfo)
        instance.plan = validated_data.get('plan', instance.plan)
        instance.completely_verified =  validated_data.get("completely_verified", instance.completely_verified)
        instance.paid =  validated_data.get("paid", instance.paid)
        instance.source = validated_data.get('source', instance.source)
        instance.is_comission = validated_data.get("is_comission", instance.is_comission)

        instance.save()
        return instance