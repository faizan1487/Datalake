from rest_framework import serializers
from .models import Alnafi_Product,IslamicAcademy_Product
from rest_framework.serializers import ModelSerializer

class AlNafiMainSiteProductSerializer(ModelSerializer):
    class Meta:
        model = Alnafi_Product
        fields = '__all__'
        
    def create(self, validated_data):
        # Get the ID of the object to update, if it exists
        product_slug = validated_data.get('product_slug')
        
        # If an ID was provided, try to get the existing object
        if product_slug:
            try:
                obj = Alnafi_Product.objects.get(product_slug=product_slug)
            except Alnafi_Product.DoesNotExist:
                obj = None
        else:
            obj = None
        
        # If the object exists, update its fields with the validated data
        if obj:
            for key, value in validated_data.items():
                setattr(obj, key, value)
            obj.save()
        else:
            obj = Alnafi_Product.objects.create(**validated_data)
        
        return obj

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
        model = IslamicAcademy_Product
        fields = ("id", "name", "slug", "date_created", "date_modified", "type", "status", "description", "price", "stock_status")