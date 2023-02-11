from rest_framework.serializers import ModelSerializer
from .models import Payment
from .models import Easypaisa_Payment

#For Stripe Payments:
class PaymentSerializer(ModelSerializer):
    class Meta:
        
        managed = False
        model = Payment
        fields = "__all__"
        

#For Easypaisa Payments:
class Easypaisa_PaymentsSerializer(ModelSerializer):
    class Meta:
        managed = False
        model = Easypaisa_Payment
        fields = '__all__'