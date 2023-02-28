from rest_framework.serializers import ModelSerializer
from .models import Payment
from .models import Easypaisa_Payment
from .models import UBL_IPG_Payment
from .models import Product

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

#For UBL IPG Payments:
class Ubl_Ipg_PaymentsSerializer(ModelSerializer):
    class Meta:
        managed = False
        model = UBL_IPG_Payment
        fields = '__all__'


#FOR PRODUCT:
class ProductSerializer(ModelSerializer):
    def __init__(self, data, fields="__all__", action="serialize"):
        self.Meta.fields = fields  # type: ignore
        if action == "deserialize":
            super().__init__(data=data)
        else:
            super().__init__(data)
    class Meta:
        model = Product
        fields = "__all__"