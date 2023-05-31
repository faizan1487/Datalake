from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from .models import UBL_IPG_Payment, AlNafi_Payment, Main_Payment,Easypaisa_Payment, Stripe_Payment, UBL_Manual_Payment
from user.models import Main_User

#For AlNafi (MainSite) Payments:
class AlNafiPaymentSerializer(ModelSerializer):
    class Meta:
        model = AlNafi_Payment
        fields = '__all__'
        
    def create(self, validated_data):
        # Get the ID of the object to update, if it exists
        my_id = validated_data.get('payment_id')
        
        # If an ID was provided, try to get the existing object
        if my_id:
            try:
                obj = AlNafi_Payment.objects.get(payment_id=my_id)
            except AlNafi_Payment.DoesNotExist:
                obj = None
        else:
            obj = None
        
        # If the object exists, update its fields with the validated data
        if obj:
            for key, value in validated_data.items():
                setattr(obj, key, value)
            obj.save()
        else:
            obj = AlNafi_Payment.objects.create(**validated_data)
        
        return obj
        
# class GetAlnafipaymentSerializer(serializers.ModelSerializer):
#     field1 = serializers.CharField()
#     field2 = serializers.CharField()

#     class Meta:
#         model = MyModel
#         fields = ('field1', 'field2')

#For Stripe Payments:
class StripePaymentSerializer(ModelSerializer):
    class Meta:
        managed = True
        model = Stripe_Payment
        fields = "__all__"
        
#For Easypaisa Payments:
class Easypaisa_PaymentsSerializer(ModelSerializer):
    class Meta:
        managed = True
        model = Easypaisa_Payment
        fields = '__all__'
    
#For UBL IPG Payments:
class Ubl_Ipg_PaymentsSerializer(ModelSerializer):
    class Meta:
        managed = True
        model = UBL_IPG_Payment
        fields = '__all__'


#For UBL-Manual Payments:
class UBL_Manual_PaymentSerializer(ModelSerializer):
    class Meta:
        # managed = True
        model = UBL_Manual_Payment
        fields = '__all__'

class MainPaymentSerializer(ModelSerializer):
    # user = MainUserSerializer('user',fields=['email'],action='deserialize')
    # user_email = SerializerMethodField()
    class Meta:
        model = Main_Payment
        fields = '__all__'
        # fields = ("alnafi_payment_id","easypaisa_ops_id","source_payment_id","user_email")
        
    # def get_user_email(self, obj):
    #     user = obj.user
    #     return user.email if user else None

class PaymentCombinedSerializer(Serializer):
    data1 = StripePaymentSerializer(many=True)
    data2 = Ubl_Ipg_PaymentsSerializer(many=True)
    data3 = Easypaisa_PaymentsSerializer(many=True)

class LocalPaymentCombinedSerializer(Serializer):
    data1 = Ubl_Ipg_PaymentsSerializer(many=True)
    data2 = Easypaisa_PaymentsSerializer(many=True)
