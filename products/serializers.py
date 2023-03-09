from rest_framework import serializers
from .models import AlnafiProduct
from rest_framework.serializers import ModelSerializer

#FOR PRODUCT:
class ProductSerializer(ModelSerializer):
    def __init__(self, data, fields="__all__", action="serialize"):
        self.Meta.fields = fields  # type: ignore
        if action == "deserialize":
            super().__init__(data=data)
        else:
            super().__init__(data)
    class Meta:
        model = AlnafiProduct
        fields = "__all__"