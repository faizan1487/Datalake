from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Alnafi_Product
from .models import IslamicAcademy_Product
from .models import Main_Product

# FOR create_or_update_main_product_from_alnafi_product Data Signal:
@receiver(post_save, sender=Alnafi_Product)
def create_or_update_main_product_from_alnafi_product(sender, instance, **kwargs):
    try:
        main_product = Main_Product.objects.get(
            source='AL-NAFI', id=instance.id)      
        main_product.amount_pkr = instance.amount_pkr
        main_product.amount_usd = instance.amount_usd
        main_product.product_language = instance.language
        main_product.allow_coupon = instance.allow_coupon
        main_product.save()
    except Main_Product.DoesNotExist:
        main_product = Main_Product(source='AL-NAFI',
                                    id=instance.id,
                                    product_name=instance.name,
                                    product_slug=instance.product_slug,
                                    product_type=instance.product_type,
                                    product_plan=instance.plan,
                                    amount_pkr=instance.amount_pkr,
                                    amount_usd=instance.amount_usd,
                                    product_language=instance.language,
                                    allow_coupon=instance.allow_coupon)
        main_product.save()


# FOR Delete_main_product_from_alnafi_product Data Signal:
@receiver(post_delete, sender=Alnafi_Product)
def delete_main_product_from_alnafi_product(sender, instance, **kwargs):
    try:
        main_product = Main_Product.objects.get(
            source='AL-NAFI', id=instance.id)
        main_product.delete()
    except Main_Product.DoesNotExist:
        pass


# FOR create_or_update_main_product_from_islamic_academy Data Signal:
@receiver(post_save, sender=IslamicAcademy_Product)
def create_or_update_main_product_from_islamic_academy(sender, instance, created, **kwargs):
    try:
        main_product = Main_Product.objects.get(
            source='ISLAMIC-ACADEMY', id=instance.id)
        main_product.product_name = instance.name
        main_product.product_slug = instance.product_slug
        main_product.created_at = instance.created_at
        main_product.modified_at = instance.modified_at
        main_product.status = instance.status
        main_product.description = instance.description
        main_product.price = instance.price
        main_product.stock_status = instance.stock_status
        main_product.save()
    except Main_Product.DoesNotExist:
        main_product = Main_Product(source='ISLAMIC-ACADEMY',
                                    id=instance.id, name=instance.name,
                                    product_slug=instance.product_slug, created_at=instance.created_at,
                                    modified_at=instance.modified_at, status=instance.status,
                                    description=instance.description, price=instance.price,
                                    stock_status=instance.stock_status
                                    )










# # main_product.product_name = instance.name
# # main_product.product_slug = instance.product_slug
# # main_product.product_type = instance.product_type
# # main_product.product_plan = instance.plan
# # main_product.created_at = 
# # main_product.modified_at = 
# # main_product.amount_pkr = instance.amount_pkr
# # main_product.amount_usd = instance.amount_usd
# # main_product.amount_gbp = 0
# # main_product.old_amount_pkr = 0 
# # main_product.old_amount_usd = 0
# # main_product.legacy_fee_pkr = 0
# # main_product.legacy_fee_usd = 0
# # main_product.legacy_available = 0 
# # main_product.qarz_product = null
# # main_product.qarz_fee_pkr = 
# # main_product.qarz_fee_usd = 
# # main_product.lms_id = 
# # main_product.product_language = 
# # main_product.has_legacy_version = 
# # main_product.is_certificate_product = 
# # main_product.allow_coupon = 
# # main_product.courses = 
# # main_product.image = 
# # main_product.bundle_Ids = 
# # main_product.status = 
# # main_product.description = 
# # main_product.stock_status = 