from django.db import models
from .models import Daily_lead
from django.db.models.signals import post_save
import requests
import json
from django.dispatch import receiver



@receiver(post_save, sender=Daily_lead)
def on_lead_saved(sender, instance, created, **kwargs):
    print("signal running")
    if instance.pk is None:
        return
    data = {
        "id": instance.id,
        "email": instance.email,
        "phone": instance.phone,
        "status": instance.status,
        "product": instance.product,
        "plan": instance.plan,
        "renewal": instance.renewal,
        "amount": instance.amount,
        "source": instance.source,
        "lead_creator": instance.lead_creator,
        "al_baseer_verify": instance.al_baseer_verify,
        "crm_verify": instance.crm_verify,
        "created_at": instance.created_at
    }
    print("data", data)
    print(f"al_baseer_verify: {instance.al_baseer_verify}, crm_verify: {instance.crm_verify}")
    if instance.al_baseer_verify == 'True' and instance.crm_verify == 'True':
        if instance.source == 'Easypaisa':
            amount = float(instance.amount)
            fees = amount*0.0085
            print("fees", fees)
            fed = fees*0.16
            print("fed", fed)
            net_amount = amount-fees-fed
            print("net_amount", net_amount)
            gst_tax = net_amount*0.05
            print("gst_tax", gst_tax)
            total_amount = round(net_amount-gst_tax)
            print("Toatl", total_amount)

            print("Easypaisa")
        elif instance.source == 'UBL-IPG':
            amount = float(instance.amount)
            fees = amount*0.024
            print("fees", fees)
            fed = fees*0.13
            print("fed", fed)
            net_amount = amount-fees-fed
            print("net_amount", net_amount)
            gst_tax = net_amount*0.05
            print("gst_tax", gst_tax)
            total_amount = round(net_amount-gst_tax)
            print("Toatl", total_amount)
            print("UBL")
        elif instance.source == 'Stripe':
            amount = float(instance.amount)
            conversion = amount*0.07
            gst_tax = conversion*0.05
            total_amount = round(conversion-gst_tax)
            # usd_amount = total_amount
            print("total", total_amount)           
        else:
            amount = float(instance.amount)
            gst_tax = amount*0.05
            total_amount = round(amount-gst_tax)
            print("total", total_amount)
        if instance.plan == 'Yearly':
            comission_amount = total_amount*0.07
            print("Yearly", comission_amount)
        elif instance.plan == 'Half Yearly':
            comission_amount = total_amount*0.06
        elif instance.plan == 'Quaterly':
            comission_amount = total_amount*0.05
            print("Quaterly", comission_amount)
        elif instance.plan == 'Monthly':
            comission_amount = total_amount*0.04
            print("Monthly", comission_amount)
        if instance.renewal == 'True':
            comission_amount = comission_amount*0.015
            print("Renewal", comission_amount)
        else:
            pass            

        url_get = f'https://crm.alnafi.com/api/resource/Leader Board For Sales?fields=["*"]'
        api_key = "4e7074f890507cb"
        api_secret = "c954faf5ff73d31"

        headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response_get = requests.get(url_get, headers=headers)
        print(response_get.text)

        if response_get.status_code == 200:
            response_data = json.loads(response_get.text)
            existing_lead_ids = [lead['daily_lead_id'] for lead in response_data['data']]
            if instance.id in existing_lead_ids:
                print(f"Lead ID {instance.id} already exists. Skipping POST request.")
            else:
                payload = {
                "daily_lead_id": instance.id,   
                "lead_owner": instance.lead_creator, 
                "earn_pkr_commission": round(comission_amount) if instance.source != 'Stripe' else 0,
                "earn_usd_commission": round(comission_amount) if instance.source == 'Stripe' else 0,  
                "payout_pkr_commission": 0,  
                "payout_usd_commission": 0, 
                "balance_pkr_commission": 0, 
                "balance_usd_commission": 0  
                }
                url = "https://crm.alnafi.com/api/resource/Leader Board For Sales"
                response = requests.post(url, headers=headers, json=payload)
                print(response.status_code)
                print(response.text)
    else:
        print("Not Verified")