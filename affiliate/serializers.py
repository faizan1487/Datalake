from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from .models  import AffiliateUser, AffiliateUniqueClick, AffiliateLead, Commission



class AffiliateSerializer(ModelSerializer):
    class Meta:
        model = AffiliateUser
        fields = '__all__'
        
    def update(self, instance, validated_data):
        # instance.source_id = validated_data.get('source_id', instance.source_id)
        # instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.first_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.country = validated_data.get('country', instance.country)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        # instance.language = validated_data.get('language', instance.language)
        # instance.referral_code = validated_data.get('referral_code', instance.referral_code)
        # instance.category_code = validated_data.get('category_code', instance.category_code)
        # instance.accept_aggrement = validated_data.get('accept_aggrement', instance.accept_aggrement)

        instance.save()
        return instance
    
class AffiliateLeadSerializer(ModelSerializer):
    class Meta:
        model = AffiliateLead
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.affiliate = validated_data.get('affiliate', instance.affiliate)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.address = validated_data.get('address', instance.address)
        instance.country = validated_data.get('country', instance.country)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance

class CommissionSerializer(ModelSerializer):
    class Meta:
        model = Commission
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.affiliate = validated_data.get('affiliate', instance.affiliate)
        instance.product = validated_data.get('product', instance.product)
        instance.amount_pkr = validated_data.get('amount_pkr', instance.amount_pkr)
        instance.amount_usd = validated_data.get('amount_usd', instance.amount_usd)
        instance.commission_usd = validated_data.get('commission_usd', instance.commission_usd)
        instance.commission_pkr = validated_data.get('commission_pkr', instance.commission_pkr)
        instance.student_email = validated_data.get('student_email', instance.student_email)
        instance.date = validated_data.get('date', instance.date)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        
        instance.save()
        return instance


class AffiliateClickSerializer(ModelSerializer):
    class Meta:
        model = AffiliateUniqueClick
        fields = '__all__'

    def update(self, instance, validated_data):
        print("update")
        instance.page_url = validated_data.get('page_url', instance.page_url)
        instance.affiliate = validated_data.get('affiliate_id', instance.affiliate)
        instance.pkr_price = validated_data.get('pkr_price', instance.pkr_price)
        instance.usd_price = validated_data.get('usd_price', instance.usd_price)

        instance.save()
        return instance