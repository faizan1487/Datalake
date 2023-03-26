from django.db import models

# Create your models here.

class Stripe_Payment(models.Model):
    payment_id = models.CharField(max_length=100 , null=True , blank=True)
    name = models.CharField(max_length=50, null=True , blank=True)
    customer_email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=50, null=True , blank=True)
    product_name = models.CharField(max_length=100, null=True , blank=True)
    amount = models.CharField(max_length=50, null=True , blank=True)
    order_datetime = models.DateTimeField(max_length=60, null=True , blank=True)
    status = models.CharField(max_length=50, null=True , blank=True)
    currency = models.CharField(max_length=50, null=True , blank=True)
    source = models.CharField(max_length=50, null=True , blank=True)
    description = models.CharField(max_length=100, null=True , blank=True)
    address = models.CharField(max_length=300, null=True , blank=True)
        
    def __str__(self):
        return self.customer_email
    
    class Meta:
        managed = True
        verbose_name = 'Stripe Payment'
        ordering = ["-order_datetime"]
        

#For Easypaisa_Payments:
class Easypaisa_Payment(models.Model):
    ops_id = models.CharField(max_length=50, null=True,blank=True)
    product_name = models.CharField(max_length=200, null=True,blank=True)
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
        return self.customer_email
   
    class Meta:
        managed = True
        verbose_name = 'Easypaisa Payment'
        ordering = ["-order_datetime"]
        

#For UBL_IPG_Payment:
class UBL_IPG_Payment(models.Model):
    # id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=50, null=False,blank=False)
    customer_email = models.EmailField(null=True,blank=True)
    card_mask = models.CharField(max_length=100, null=True,blank=True)
    product_name = models.CharField(max_length=50, null=True,blank=True)
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
        return self.customer_email

    class Meta:
        managed = True
        verbose_name = "UBL IPG Payment"
        ordering = ["-order_datetime"]