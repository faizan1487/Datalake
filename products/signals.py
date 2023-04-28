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
        main_product.product_name = instance.name
        main_product.product_slug = instance.product_slug
        main_product.product_type = instance.product_type
        main_product.product_plan = instance.plan
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


