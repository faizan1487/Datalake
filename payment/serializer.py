from rest_framework.serializers import ModelSerializer
from .models import Payment
class PaymentSerializer(ModelSerializer):
    class Meta:
        
        managed = False
        model = Payment
        fields = "__all__"
        