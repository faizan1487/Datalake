from rest_framework.serializers import ModelSerializer
from .models import Stripe_Payment
from .models import Easypaisa_Payment
from .models import UBL_Manual_Payment
from .models import UBL_IPG_Payment, AlNafi_Payment




#For AlNafi (MainSite) Payments:
class AlNafiPaymentSerializer(ModelSerializer):
    class Meta:
        model = AlNafi_Payment
        fields = '__all__'

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
        managed = True
        model = UBL_Manual_Payment
        fields = '__all__'
