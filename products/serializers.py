from rest_framework import serializers
from .models import Alnafi_Product
from .models import IslamicAcademyProduct
from rest_framework.serializers import ModelSerializer

class AlNafiMainSiteProductSerializer(ModelSerializer):
    class Meta:
        model = Alnafi_Product
        fields = '__all__'

# #FOR AL-NAFI MAIN SITE PRODUCT:
# class AlnafiProductSerializer(ModelSerializer):
#     def __init__(self, data, fields="__all__", action="serialize"):
#         self.Meta.fields = fields  # type: ignore
#         if action == "deserialize":
#             super().__init__(data=data)
#         else:
#             super().__init__(data)
#     class Meta:
#         model = Alnafi_Product
#         fields = "__all__"


#FOR ISLAMIC ACADEMY PRODUCT:
class IslamicAcademyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = IslamicAcademyProduct
        fields = ("id", "name", "slug", "date_created", "date_modified", "type", "status", "description", "price", "stock_status")