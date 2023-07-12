from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField, ValidationError
from .models import UBL_IPG_Payment, AlNafi_Payment, Main_Payment,Easypaisa_Payment, Stripe_Payment, UBL_Manual_Payment
from user.models import Main_User

#For AlNafi (MainSite) Payments:
class AlNafiPaymentSerializer(ModelSerializer):
    class Meta:
        model = AlNafi_Payment
        fields = '__all__'

    def update(self, instance, validated_data):
        # instance.customer_email = validated_data.get('customer_email', instance.customer_email)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.amount_pkr = validated_data.get('amount_pkr', instance.amount_pkr)
        instance.amount_usd = validated_data.get('amount_usd', instance.amount_usd)
        instance.order_datetime = validated_data.get('order_datetime', instance.order_datetime)
        instance.expiration_datetime = validated_data.get('expiration_datetime', instance.expiration_datetime)
        instance.source = validated_data.get('source', instance.source)
        instance.order_id = validated_data.get('order_id', instance.order_id)
        instance.date_of_activation = validated_data.get('date_of_activation', instance.date_of_activation)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.qarz = validated_data.get('qarz', instance.qarz)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        instance.payment_proof = validated_data.get('payment_proof', instance.payment_proof)
        instance.send_invoice = validated_data.get('send_invoice', instance.send_invoice)
        instance.pk_invoice_number = validated_data.get('pk_invoice_number', instance.pk_invoice_number)
        instance.us_invoice_number = validated_data.get('us_invoice_number', instance.us_invoice_number)
        instance.sponsored = validated_data.get('sponsored', instance.sponsored)
        instance.coupon_code = validated_data.get('coupon_code', instance.coupon_code)
        instance.is_upgrade_payment = validated_data.get('is_upgrade_payment', instance.is_upgrade_payment)
        instance.affiliate = validated_data.get('affiliate', instance.affiliate)

        instance.save()
        return instance

        
    


class UBL_Manual_PaymentSerializer(ModelSerializer):
    class Meta:
        # managed = True
        model = UBL_Manual_Payment
        fields = '__all__'
    

    def update(self, instance, validated_data):
        instance.candidate_name = validated_data.get('candidate_name', instance.candidate_name)
        instance.depositor_name = validated_data.get('depositor_name', instance.depositor_name)
        instance.customer_email = validated_data.get('customer_email', instance.customer_email)
        instance.candidate_phone = validated_data.get('candidate_phone', instance.candidate_phone)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.status = validated_data.get('status', instance.status)
        instance.deposit_date = validated_data.get('deposit_date', instance.deposit_date)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.payment_channel = validated_data.get('payment_channel', instance.payment_channel)
        instance.source = validated_data.get('source', instance.source)
        instance.transaction_image = validated_data.get('transaction_image', instance.transaction_image)

        instance.save()
        return instance


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
