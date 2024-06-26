from enum import unique
from django.db import models
from datetime import datetime, timezone
from user.models import Main_User
from products.models import Main_Product
# Create your models here.


#For MainSite(Al-Nafi) Payments:
class AlNafi_Payment(models.Model):
    payment_id = models.IntegerField(null=True, blank=False)
    customer_email = models.CharField(max_length=300, null=True, blank=False)
    product_name = models.JSONField(null=True, blank=True)
    amount_pkr = models.IntegerField(default=0)
    amount_usd = models.IntegerField(default=0)
    expiration_datetime = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=150, null=True, blank=True)
    order_id = models.CharField(max_length=150, null=True, blank=False)
    date_of_activation = models.DateField(null=True, blank=True)
    qarz = models.BooleanField(default=False)
    remarks = models.CharField(max_length=1000,null=True, blank=True)
    payment_proof = models.CharField(max_length=150, null=True, blank=True)
    send_invoice = models.BooleanField(default=True, null=True, blank=True)
    pk_invoice_number= models.CharField(max_length = 101,null=True,blank=True)
    us_invoice_number= models.CharField(max_length = 101,null=True,blank=True)
    sponsored = models.BooleanField(default=False)
    coupon_code = models.CharField(max_length=200, null=True, blank=True)
    is_upgrade_payment = models.BooleanField(default=False)
    affiliate = models.CharField(max_length=200,null=True, blank=True)
    # erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    erp_lead = models.CharField(max_length=255,blank=True, null=True)

    created_at= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    order_datetime = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return f"{self.customer_email}"

    class Meta:
        managed = True
        verbose_name = "Al-Nafi Payment"
        ordering = ["-order_datetime"]


class New_Alnafi_Payments(models.Model):
    orderId = models.CharField(max_length=255)
    amount = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    card_number = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    meta = models.JSONField(null=True, blank=True)
    payment_method_name = models.CharField(max_length=255, blank=True, null=True)
    payment_method_currency = models.CharField(max_length=255, blank=True, null=True)
    payment_method_source_name = models.CharField(max_length=255, blank=True, null=True)
    product_names = models.JSONField(null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    pk_invoice_number = models.CharField(max_length=255, blank=True, null=True)
    us_invoice_number = models.CharField(max_length=255, blank=True, null=True)
    send_invoice = models.BooleanField(default=False)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    depositor_name = models.CharField(max_length=255, blank=True, null=True)
    application_id = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.CharField(max_length=300, null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    coupon_id = models.CharField(max_length=255, blank=True, null=True)
    additional_months = models.IntegerField(null=True, blank=True)
    is_manual = models.BooleanField(default=False)
    amount_pkr = models.IntegerField(null=True, blank=True)
    amount_usd = models.IntegerField(null=True, blank=True)
    webhook_called = models.BooleanField(default=False)
    old_payments = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=1000,null=True, blank=True)
    transaction_id = models.CharField(max_length=255,null=True, blank=True)

    payment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = "New Al-Nafi Payment"

    def _str_(self):
        return self.orderId or '-'



class Unpaid_New_Alnafi_Payments(models.Model):
    orderId = models.CharField(max_length=255,unique=True)
    amount = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    card_number = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    meta = models.JSONField(null=True, blank=True)
    payment_method_name = models.CharField(max_length=255, blank=True, null=True)
    payment_method_currency = models.CharField(max_length=255, blank=True, null=True)
    payment_method_source_name = models.CharField(max_length=255, blank=True, null=True)
    product_names = models.JSONField(null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    pk_invoice_number = models.CharField(max_length=255, blank=True, null=True)
    us_invoice_number = models.CharField(max_length=255, blank=True, null=True)
    send_invoice = models.BooleanField(default=False)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    depositor_name = models.CharField(max_length=255, blank=True, null=True)
    application_id = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.CharField(max_length=300, null=True, blank=True)
    coupon_id = models.CharField(max_length=255, blank=True, null=True)
    additional_months = models.IntegerField(null=True, blank=True)
    is_manual = models.BooleanField(default=False)
    amount_pkr = models.IntegerField(null=True, blank=True)
    amount_usd = models.IntegerField(null=True, blank=True)
    webhook_called = models.BooleanField(default=False)
    old_payments = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=1000,null=True, blank=True)
    transaction_id = models.CharField(max_length=255,null=True, blank=True)

    expiration_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = "Unpaid New Al-Nafi Payment"

    def _str_(self): 
        return self.orderId or '-'



#For UBL Manual Payments:
class UBL_Manual_Payment(models.Model):
    candidate_name = models.CharField(max_length=200, null=True, blank=True)
    depositor_name = models.CharField(max_length=200, null=True, blank=True)
    customer_email = models.CharField(max_length=200, null=True, blank=True)
    candidate_phone = models.CharField(max_length=45, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    product_name = models.JSONField(null=True, blank=True)
    status = models.BooleanField(default=False)
    deposit_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True ,null=True, blank=True)
    payment_channel = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.CharField(max_length=250, null=True, blank=True)
    source = models.CharField(max_length=45, null=True, blank=True)
    transaction_image = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"{self.customer_email}"

    class Meta:
        managed = True
        verbose_name = "UBL-Manual Payment"
        ordering = ["-deposit_date"]

#For UBL_IPG_Payment:
class UBL_IPG_Payment(models.Model):
    # id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=50, null=False,blank=False)
    customer_email = models.EmailField(null=True,blank=True)
    card_mask = models.CharField(max_length=100, null=True,blank=True)
    product_name = models.JSONField(null=True, blank=True)
    order_datetime = models.DateTimeField(max_length=60, null=False , blank=False)
    order_id = models.CharField(max_length=100, null=False,blank=False)
    amount = models.CharField(max_length=50, null=True,blank=True)
    captured = models.CharField(max_length=50, null=True,blank=True)
    reversed = models.CharField(max_length=50, null=True,blank=True)
    refund = models.CharField(max_length=50, null=True , blank=True)
    approval_code = models.CharField(max_length=50, null=True,blank=True)
    source = models.CharField(max_length=50, null=True,blank=True)
    status = models.CharField(max_length=50, null=True,blank=True)

    def __str__(self):
        return f"{self.customer_email}"

    class Meta:
        managed = True
        verbose_name = "UBL IPG Payment"
        ordering = ["-order_datetime"]


#For Easypaisa_Payments:
class Easypaisa_Payment(models.Model):
    ops_id = models.CharField(max_length=50, null=True,blank=True)
    product_name = models.JSONField(null=True, blank=True)
    order_id = models.CharField(max_length=50, null=True,blank=True)
    transaction_id = models.CharField(max_length=50, null=True,blank=True)
    order_datetime = models.DateTimeField(default=None, null=False , blank=False)
    customer_msidn = models.CharField(max_length=50, null=True,blank=True)
    customer_email = models.EmailField(null=True,blank=True)
    amount = models.CharField(max_length=50, null=True,blank=True)
    status = models.CharField(max_length=50, null=True,blank=True)
    source = models.CharField(max_length=50, null=True , blank=True)
    credit_card = models.CharField(max_length=50, null=True,blank=True)
    bin_bank_name = models.CharField(max_length=50, null=True,blank=True)
    fee_pkr = models.CharField(max_length=50, null=True,blank=True)
    fed_pkr = models.CharField(max_length=50, null=True,blank=True)
    error_reason = models.CharField(max_length=200, null=True,blank=True)
    token_paid_datetime = models.DateTimeField(default=None, null=False , blank=False)

    def __str__(self):
        return f"{self.customer_email}"

    class Meta:
        managed = True
        verbose_name = 'Easypaisa Payment'
        ordering = ["-order_datetime"]


#For Stripe Payments:
class Stripe_Payment(models.Model):
    payment_id = models.CharField(max_length=100 , null=True , blank=True)
    alnafi_order_id = models.CharField(max_length=100 , null=True , blank=True)
    name = models.CharField(max_length=50, null=True , blank=True)
    customer_email = models.CharField(null=True,blank=True, max_length=150)
    phone = models.CharField(max_length=50, null=True , blank=True)
    product_name = models.JSONField(null=True, blank=True)
    amount = models.CharField(max_length=50, null=True , blank=True)
    order_datetime = models.DateTimeField(max_length=60, null=True , blank=True)
    status = models.CharField(max_length=50, null=True , blank=True)
    currency = models.CharField(max_length=50, null=True , blank=True)
    source = models.CharField(max_length=50, null=True , blank=True)
    description = models.CharField(max_length=100, null=True , blank=True)
    address = models.CharField(max_length=300, null=True , blank=True)

    def __str__(self):
        return f"{self.customer_email}"

    class Meta:
        managed = True
        verbose_name = 'Stripe Payment'
        ordering = ["-order_datetime"]



#FOR MURGED ALL PAYMENT IN ONE TABLE MAIN_PAYMENT:
class Main_Payment(models.Model):
    source_payment_id = models.CharField(max_length=100 , null=True , blank=True)
    alnafi_payment_id = models.CharField(max_length=50, null=True,blank=True)
    easypaisa_ops_id = models.CharField(max_length=50, null=True,blank=True)
    easypaisa_customer_msidn = models.CharField(max_length=50, null=True,blank=True)
    card_mask = models.CharField(max_length=100, null=True,blank=True)
    user =  models.ForeignKey(Main_User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_payments")
    product = models.ManyToManyField(Main_Product, related_name="product_payments", blank=True)
    # product = models.ForeignKey(Main_Product, on_delete=models.SET_NULL, null=True, related_name="product_payments", blank=True)
    amount = models.CharField(max_length=50, null=True,blank=True)
    currency = models.CharField(max_length=50, null=True , blank=True)
    source = models.CharField(max_length=50, null=True , blank=True)
    internal_source = models.CharField(max_length=50, null=True , blank=True)
    status = models.CharField(max_length=50, null=True , blank=True)
    order_datetime = models.DateTimeField(null=True , blank=True)
    expiration_datetime = models.DateTimeField(null=True, blank=True)
    activation_datetime = models.DateTimeField(null=True, blank=True)
    token_paid_datetime = models.DateTimeField(null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    easypaisa_fee_pkr = models.CharField(max_length=50, null=True,blank=True)
    easypaisa_fed_pkr = models.CharField(max_length=50, null=True,blank=True)
    ubl_captured = models.CharField(max_length=50, null=True,blank=True)
    ubl_reversed = models.CharField(max_length=50, null=True,blank=True)
    ubl_refund = models.CharField(max_length=50, null=True , blank=True)
    ubl_approval_code = models.CharField(max_length=50, null=True,blank=True)
    description = models.CharField(max_length=300, null=True , blank=True)
    qarz = models.BooleanField(default=False)
    remarks = models.CharField(max_length=1000,null=True, blank=False)
    payment_proof = models.CharField(max_length=200, null=True, blank=False)
    send_invoice = models.BooleanField(default=True, null=True, blank=True)
    pk_invoice_number = models.CharField(max_length = 10,null=True,blank=True)
    us_invoice_number = models.CharField(max_length = 10,null=True,blank=True)
    sponsored = models.BooleanField(default=False)
    coupon_code = models.CharField(max_length=20, null=True, blank=False)
    is_upgrade_payment = models.BooleanField(default=False)
    affiliate = models.CharField(max_length=50,null=True, blank=False)
    candidate_name = models.CharField(max_length=200, null=True, blank=True)
    ubl_depositor_name = models.CharField(max_length=200, null=True, blank=True)
    candidate_phone = models.CharField(max_length=45, null=True, blank=True)
    bin_bank_name = models.CharField(max_length=50, null=True,blank=True)
    error_reason = models.CharField(max_length=200, null=True,blank=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=200, null=True,blank=True)

    class Meta:
        managed = True
        verbose_name = "Main Payment"
        ordering = ["-order_datetime"]

    def __str__(self):
        return f"ID: {self.id}"


class NavbarLink(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    path = models.CharField(max_length=100,null=True, blank=True)
    image = models.ImageField(upload_to='navbar_images')
    group = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name



class Renewal(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null= True)
    last_name = models.CharField(max_length=100, blank=True, null= True)
    user_id = models.CharField(max_length=100, blank=True, null= True)
    phone = models.CharField(max_length=100, blank=True, null= True)
    country = models.CharField(max_length=100, blank=True, null= True)
    address = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.CharField(max_length=100, null=True, blank=True)
    payment_date = models.CharField(max_length=100, null=True, blank=True)
    expiration_date = models.CharField(max_length=100, null=True, blank=True)
    product_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user_id}"
    
    # class Meta:
    #     managed = True
    #     verbose_name = "Renewal Leads"