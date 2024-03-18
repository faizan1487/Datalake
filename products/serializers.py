from rest_framework import serializers
from .models import Alnafi_Product,IslamicAcademy_Product
from rest_framework.serializers import ModelSerializer

class AlNafiMainSiteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alnafi_Product
        fields = (
            'id',
            'image',
            'product_type',
            'product_slug',
            'plan',
            'name',
            'bundle_Ids',
            'amount_pkr',
            'amount_usd',
            'amount_gbp',
            'old_amount_pkr',
            'old_amount_usd',
            'legacy_fee_pkr',
            'legacy_fee_usd',
            'legacy_available',
            'qarz_product',
            'qarz_fee_pkr',
            'qarz_fee_usd',
            'lms_id',
            'language',
            'created_at',
            'has_legacy_version',
            'is_certificate_product',
            'allow_coupon',
            'courses',
        )

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.product_type = validated_data.get('product_type', instance.product_type)
        instance.product_slug = validated_data.get('product_slug', instance.product_slug)
        instance.plan = validated_data.get('plan', instance.plan)
        instance.name = validated_data.get('name', instance.name)
        instance.bundle_Ids = validated_data.get('bundle_Ids', instance.bundle_Ids)
        instance.amount_pkr = validated_data.get('amount_pkr', instance.amount_pkr)
        instance.amount_usd = validated_data.get('amount_usd', instance.amount_usd)
        instance.amount_gbp = validated_data.get('amount_gbp', instance.amount_gbp)
        instance.old_amount_pkr = validated_data.get('old_amount_pkr', instance.old_amount_pkr)
        instance.old_amount_usd = validated_data.get('old_amount_usd', instance.old_amount_usd)
        instance.legacy_fee_pkr = validated_data.get('legacy_fee_pkr', instance.legacy_fee_pkr)
        instance.legacy_fee_usd = validated_data.get('legacy_fee_usd', instance.legacy_fee_usd)
        instance.legacy_available = validated_data.get('legacy_available', instance.legacy_available)
        instance.qarz_product = validated_data.get('qarz_product', instance.qarz_product)
        instance.qarz_fee_pkr = validated_data.get('qarz_fee_pkr', instance.qarz_fee_pkr)
        instance.qarz_fee_usd = validated_data.get('qarz_fee_usd', instance.qarz_fee_usd)
        instance.lms_id = validated_data.get('lms_id', instance.lms_id)
        instance.language = validated_data.get('language', instance.language)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.has_legacy_version = validated_data.get('has_legacy_version', instance.has_legacy_version)
        instance.is_certificate_product = validated_data.get('is_certificate_product', instance.is_certificate_product)
        instance.allow_coupon = validated_data.get('allow_coupon', instance.allow_coupon)
        instance.courses = validated_data.get('courses', instance.courses)
        
        instance.save()
        return instance

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

# FOR MAIN PRODUCTS COMBINE PRODUCT ALL TABLE IN ONE:
