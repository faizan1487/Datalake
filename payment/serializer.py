from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField, ValidationError
from .models import UBL_IPG_Payment, AlNafi_Payment, Main_Payment,Easypaisa_Payment, Stripe_Payment, UBL_Manual_Payment, New_Alnafi_Payments
from user.models import Main_User

#For AlNafi (MainSite) Payments:
class AlNafiPaymentSerializer(ModelSerializer):
    class Meta:
        model = AlNafi_Payment
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.customer_email = validated_data.get('customer_email', instance.customer_email)
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


class New_Al_Nafi_Payments_Serializer(ModelSerializer):
    class Meta:
        model = New_Alnafi_Payments
        fields = '__all__'

    def update(self, instance, validated_data):
        # instance.customer_id = validated_data.get('customer_id', instance.customer_id)
        # instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.customer_email = validated_data.get('customer_email', instance.customer_email)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        # instance.phone = validated_data.get('phone', instance.phone)
        # instance.affiliate_code = validated_data.get('affiliate_code', instance.affiliate_code)
        instance.coupon_id = validated_data.get('coupon_id', instance.coupon_id)
        # instance.application = validated_data.get('application', instance.application)
        # instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.payment_method_currency = validated_data.get('payment_method_source', instance.payment_method_currency)
        instance.payment_method_source_name = validated_data.get('payment_method_source', instance.payment_method_source_name)
        # instance.product_ids = validated_data.get('product_ids', instance.product_ids)
        # instance.product_data = validated_data.get('product_data', instance.product_data)
        instance.product_names = validated_data.get('product_names', instance.product_names)
        # instance.product_amount = validated_data.get('product_amount', instance.product_amount)
        instance.orderId = validated_data.get('orderId', instance.orderId)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.amount_pkr = validated_data.get('amount_pkr', instance.amount_pkr)
        instance.amount_usd = validated_data.get('amount_usd', instance.amount_usd)
        instance.country = validated_data.get('country', instance.country)
        instance.status = validated_data.get('status', instance.status)
        # instance.payment_proof = validated_data.get('payment_proof', instance.payment_proof)
        instance.card_number = validated_data.get('card_number', instance.card_number)
        instance.account_number = validated_data.get('account_number', instance.account_number)
        instance.send_invoice = validated_data.get('send_invoice', instance.send_invoice)
        instance.pk_invoice_number = validated_data.get('pk_invoice_number', instance.pk_invoice_number)
        instance.us_invoice_number = validated_data.get('us_invoice_number', instance.us_invoice_number)
        instance.meta = validated_data.get('meta', instance.meta)
        instance.depositor_name = validated_data.get('depositor_name', instance.depositor_name)
        instance.purpose = validated_data.get('purpose', instance.purpose)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.additional_months = validated_data.get('additional_months', instance.additional_months)
        # instance.dynamic_checkout_link = validated_data.get('dynamic_checkout_link', instance.dynamic_checkout_link)
        instance.is_manual = validated_data.get('is_manual', instance.is_manual)
        instance.webhook_called = validated_data.get('webhook_called', instance.webhook_called)
        instance.old_payments = validated_data.get('old_payments', instance.old_payments)
        instance.remarks = validated_data.get('remarks', instance.remarks)
    
        instance.payment_date = validated_data.get('payment_date', instance.payment_date)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        

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
