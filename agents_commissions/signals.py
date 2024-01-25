from django.db import models
from .models import Daily_lead, Daily_Sales_Support
from django.db.models.signals import post_save
import requests
import json
from django.dispatch import receiver



@receiver(post_save, sender=Daily_lead)
def on_lead_saved(sender, instance, created, **kwargs):
    # print("signal running")
    if instance.pk is None:
        return
    # data = {
    #     "id": instance.id,
    #     "email": instance.email,
    #     "phone": instance.phone,
    #     "status": instance.status,
    #     "product": instance.product,
    #     "plan": instance.plan,
    #     "renewal": instance.renewal,
    #     "amount": instance.amount,
    #     "source": instance.source,
    #     "lead_creator": instance.lead_creator,
    #     "al_baseer_verify": instance.al_baseer_verify,
    #     "crm_verify": instance.crm_verify,
    #     "created_at": instance.created_at
    # }
    # print("data", data)
    # print(f"al_baseer_verify: {instance.al_baseer_verify}, crm_verify: {instance.crm_verify}")
    if instance.manager_approval.lower() == 'true' and instance.manager_approval_crm.lower() == 'true' and instance.veriification_cfo.lower() == 'true':
        # print("in condition")
        if instance.source == 'Easypaisa':
            amount = float(instance.amount)
            fees = amount*0.0085       #0.0085 = 0.85%
            # print("fees", fees)
            fed = fees*0.16            #0.16 = 16%
            # print("fed", fed)
            net_amount = amount-fees-fed
            # print("net_amount", net_amount)
            gst_tax = net_amount*0.05   #0.05 = 5%
            # print("gst_tax", gst_tax)
            total_amount = round(net_amount-gst_tax)
            # print("Toatl", total_amount)

            # print("Easypaisa")
        elif instance.source == 'UBL-IPG':
            amount = float(instance.amount)
            fees = amount*0.024   #0.024 = 2.4%
            # print("fees", fees)
            fed = fees*0.13       #0.13 = 13%
            # print("fed", fed)
            net_amount = amount-fees-fed
            # print("net_amount", net_amount)
            gst_tax = net_amount*0.05 
            # print("gst_tax", gst_tax)
            total_amount = round(net_amount-gst_tax)
            # print("Toatl", total_amount)
            # print("UBL")
        elif instance.source == 'Stripe':
            amount = float(instance.amount)
            conversion = amount*0.07    #0.07 = 7%
            gst_tax = conversion*0.05
            total_amount = round(conversion-gst_tax)
            # usd_amount = total_amount
            # print("total", total_amount)           
        else:
            amount = float(instance.amount)
            gst_tax = amount*0.05
            total_amount = round(amount-gst_tax)
            # print("total", total_amount)
        if instance.plan == 'Yearly':
            comission_amount = total_amount*0.07
            # print("Yearly", comission_amount)
        elif instance.plan == 'Half Yearly':
            comission_amount = total_amount*0.06
        elif instance.plan == 'Quaterly':
            comission_amount = total_amount*0.05
            # print("Quaterly", comission_amount)
        elif instance.plan == 'Monthly':
            comission_amount = total_amount*0.04
            # print("Monthly", comission_amount)
        elif instance.plan == 'Easy Pay Program':
            comission_amount = total_amount*0.02
            # print("In Elif", comission_amount)
        if instance.renewal == 'True':
            comission_amount = total_amount*0.015
            # print("Renewal", comission_amount)
        else:
            pass            
        # print("Commission", comission_amount)
        # print("Source", instance.source)

        url_get = f'https://crm.alnafi.com/api/resource/Leader Board For Sales?fields=["*"]'
        api_key = "4e7074f890507cb"
        api_secret = "c954faf5ff73d31"

        headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response_get = requests.get(url_get, headers=headers)
        # print(response_get.text)
        # print("source", instance.source)
        if response_get.status_code == 200:
            response_data = json.loads(response_get.text)
            existing_lead = next((lead for lead in response_data['data'] if lead['lead_owner'] == instance.lead_creator), None)
            if existing_lead:
            # Lead_owner exists, make a PUT request to update the existing record
                lead_id = existing_lead['name']  # Assuming 'name' is the field that holds the lead ID
                url_put = f'https://crm.alnafi.com/api/resource/Leader Board For Sales/{lead_id}'
                existing_earn_pkr = float(existing_lead.get('earn_pkr_commission', 0))
                existing_earn_usd = float(existing_lead.get('earn_usd_commission', 0))
                existing_amount = float(existing_lead.get('total_revenue',0))
                existing_usd_revenue = float(existing_lead.get('total_usd_revenue', 0))
    
                # print("Existing", existing_amount)
                instance_amount = float(instance.amount)
                # print("source", instance.source)
                payload = {
                    "earn_pkr_commission": round(comission_amount + existing_earn_pkr) if instance.source not in ['Stripe', 'dlocal'] else existing_earn_pkr,
                    "earn_usd_commission": round(comission_amount + existing_earn_usd) if instance.source in ['Stripe', 'dlocal'] else existing_earn_usd,
                    "total_revenue": round(instance_amount + existing_amount) if instance.source not in ['Stripe', 'dlocal'] else existing_amount,
                    "total_usd_revenue": round(instance_amount + existing_usd_revenue) if instance.source in ['Stripe', 'dlocal'] else existing_usd_revenue,
                    # Add other fields you want to update
                }
                response_put = requests.put(url_put, headers=headers, json=payload)
                # print(response_put.text)
                # print("Response", response_put)
            else:
                payload = {
                "daily_lead_id": instance.id,   
                "lead_owner": instance.lead_creator, 
                "earn_pkr_commission": round(comission_amount) if instance.source not in ['Stripe', 'dlocal'] else 0,
                "earn_usd_commission": round(comission_amount) if instance.source in ['Stripe', 'dlocal'] else 0,  
                "total_revenue": instance.amount if instance.source not in ['Stripe', 'dlocal'] else 0,
                "total_usd_revenue": instance.amount if instance.source in ['Stripe', 'dlocal'] else 0,
                "payout_pkr_commission": 0,  
                "payout_usd_commission": 0, 
                "balance_pkr_commission": 0, 
                "balance_usd_commission": 0  
                }
                url = "https://crm.alnafi.com/api/resource/Leader Board For Sales"
                response = requests.post(url, headers=headers, json=payload)
                # print(response.status_code)
                # print(response.text)
                # return response("Done")
    else:
        print("Not Verified")

@receiver(post_save, sender=Daily_Sales_Support)
def on_support_saved(sender, instance, created, **kwargs):
    # print("signal running")
    if instance.pk is None:
        return
    if instance.manager_approval == 'True' and instance.manager_approval_crm == 'True' and instance.veriification_cfo == 'True':
        if instance.source == 'Easypaisa':
            amount = float(instance.amount)
            fees = amount*0.0085       #0.0085 = 0.85%
            # print("fees", fees)
            fed = fees*0.16            #0.16 = 16%
            # print("fed", fed)
            net_amount = amount-fees-fed
            # print("net_amount", net_amount)
            gst_tax = net_amount*0.05   #0.05 = 5%
            # print("gst_tax", gst_tax)
            total_amount = round(net_amount-gst_tax)
            # print("Toatl", total_amount)

            # print("Easypaisa")
        elif instance.source == 'UBL-IPG':
            amount = float(instance.amount)
            fees = amount*0.024   #0.024 = 2.4%
            # print("fees", fees)
            fed = fees*0.13       #0.13 = 13%
            # print("fed", fed)
            net_amount = amount-fees-fed
            # print("net_amount", net_amount)
            gst_tax = net_amount*0.05 
            # print("gst_tax", gst_tax)
            total_amount = round(net_amount-gst_tax)
            # print("Toatl", total_amount)
            # print("UBL")
        elif instance.source == 'Stripe':
            amount = float(instance.amount)
            conversion = amount*0.07    #0.07 = 7%
            gst_tax = conversion*0.05
            total_amount = round(conversion-gst_tax)
            # usd_amount = total_amount
            # print("total", total_amount)           
        else:
            amount = float(instance.amount)
            gst_tax = amount*0.05
            total_amount = round(amount-gst_tax)
            # print("total", total_amount)
        comission_amount = total_amount*0.02
        # print('comission', comission_amount)
        url_get = f'https://crm.alnafi.com/api/resource/Leader Board For Support?fields=["*"]'
        api_key = "4e7074f890507cb"
        api_secret = "c954faf5ff73d31"

        headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response_get = requests.get(url_get, headers=headers)
        # print(response_get.text)

        if response_get.status_code == 200:
            response_data = json.loads(response_get.text)
            existing_lead = next((lead for lead in response_data['data'] if lead['lead_owner'] == instance.lead_creator), None)
            if existing_lead:
            # Lead_owner exists, make a PUT request to update the existing record
                lead_id = existing_lead['name']  # Assuming 'name' is the field that holds the lead ID
                url_put = f'https://crm.alnafi.com/api/resource/Leader Board For Support/{lead_id}'
                existing_earn_pkr = float(existing_lead.get('earn_pkr_commission', 0))
                existing_earn_usd = float(existing_lead.get('earn_usd_commission', 0))
                existing_amount = float(existing_lead.get('total_revenue',0))
                # print("Existing", existing_amount)
                instance_amount = float(instance.amount)
                payload = {
                    "earn_pkr_commission": round(comission_amount + existing_earn_pkr) if instance.source != 'Stripe' else existing_earn_pkr,
                    "earn_usd_commission": round(comission_amount + existing_earn_usd) if instance.source == 'Stripe' else existing_earn_usd,
                    "total_revenue": round(instance_amount + existing_amount)
                    # Add other fields you want to update
                }
                response_put = requests.put(url_put, headers=headers, json=payload)
            else:
                payload = {
                "daily_lead_id": instance.id,   
                "lead_owner": instance.lead_creator, 
                "earn_pkr_commission": round(comission_amount) if instance.source != 'Stripe' else 0,
                "earn_usd_commission": round(comission_amount) if instance.source == 'Stripe' else 0,  
                "total_revenue": instance.amount,
                "payout_pkr_commission": 0,  
                "payout_usd_commission": 0, 
                "balance_pkr_commission": 0, 
                "balance_usd_commission": 0  
                }
                url = "https://crm.alnafi.com/api/resource/Leader Board For Support"
                response = requests.post(url, headers=headers, json=payload)
                # print(response.status_code)
                # print(response.text)
                # return response("Done")
    else:
        print("Not Verified")
        