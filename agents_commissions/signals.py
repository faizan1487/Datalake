from django.db import models
from .models import Daily_lead, Daily_Sales_Support, Deleted_Daily_lead, Deleted_Daily_Sales_Support
from django.db.models.signals import post_save, post_delete
import requests
import json
from threading import Thread
from django.dispatch import receiver




@receiver(post_save, sender=Daily_lead)
def commission_making_sales(sender, instance, created, **kwargs):
    thread = Thread(target=on_lead_saved, args=(sender, instance, created), kwargs=kwargs)
    thread.start()
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
    # print(instance.completely_verified)
    if instance.manager_approval == 'True' and instance.manager_approval_crm == 'True' and instance.veriification_cfo == 'True' and instance.completely_verified == '1' and instance.paid == '0':
        # instance.is_comission = True
        # instance.save()
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
            change = amount - conversion
            gst_tax = change*0.13
            total_amount = round(change-gst_tax)
            # usd_amount = total_amount
            # print("total", total_amount)           
        else:
            amount = float(instance.amount)
            gst_tax = amount*0.05
            total_amount = round(amount-gst_tax)
            # print("total", total_amount)
        
        if instance.is_exam_fee is not None and instance.is_exam_fee.lower() == 'true':
            comission_amount = total_amount*0
        elif instance.support is not None and instance.support.lower() == 'true':
            comission_amount = total_amount*0.02
        else:
            # print("plan")
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
                # print("in else")
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

@receiver(post_save, sender=Daily_lead)
def commission_deduction_sales(sender, instance, **kwargs):
    thread = Thread(target=deduct_from_leader_board, args=(sender, instance), kwargs=kwargs)
    thread.start()
def deduct_from_leader_board(sender, instance, **kwargs):
    print("signal running")
    # print("veriification_cfo", instance.veriification_cfo)
    # print("instance.is_comission",instance.is_comission)
    if instance.is_comission:
        if instance.veriification_cfo == 'Deduct Commission Due Some Cause' or instance.paid == '1':
            # print("in condition")
            try:
                lead_creator = instance.lead_creator
                # print("instance.lead_creator",  lead_creator)
                if lead_creator:
                    amount_to_deduct = float(instance.amount)
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
                    change = amount - conversion
                    gst_tax = change*0.13
                    total_amount = round(change-gst_tax)
                    # usd_amount = total_amount
                    # print("total", total_amount)           
                else:
                    amount = float(instance.amount)
                    gst_tax = amount*0.05
                    total_amount = round(amount-gst_tax)
                    # print("total", total_amount)

                if instance.support.lower() == 'true':
                    comission_amount = total_amount*0.02
                else:
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

                # print("amont", amount_to_deduct)
                url_get = 'https://crm.alnafi.com/api/resource/Leader Board For Sales?fields=["*"]'
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
                    response_data = response_get.json()
                    # print("response data", response_data)
                    for lead_entry in response_data['data']:
                        if lead_entry.get('lead_owner') == lead_creator:
                            # print("Owner", lead_entry.get('lead_owner'))
                            # print(lead_entry.get('earn_pkr_commission'))
                            # print(lead_entry.get('total_usd_revenue'))
                            # print("source", instance.source)
                            payload = {}
                            if instance.source in ['dlocal', 'Stripe']:
                                payload["earn_usd_commission"] = max(round(float(lead_entry.get('earn_usd_commission', 0)) - comission_amount), 0)
                                payload["total_usd_revenue"] = max(round(float(lead_entry.get('total_usd_revenue', 0)) - amount_to_deduct), 0)
                            else:
                                # print("in else")
                                payload["earn_pkr_commission"] = max(round(float(lead_entry.get('earn_pkr_commission', 0)) - comission_amount), 0)
                                payload["total_revenue"] = max(round(float(lead_entry.get('total_revenue', 0)) - amount_to_deduct), 0)
                            # print("payload", payload)
                            url_put = f'https://crm.alnafi.com/api/resource/Leader Board For Sales/{lead_entry["name"]}'
                            response_put = requests.put(url_put, headers=headers, json=payload)
                            # print(response_put.text)
                            if response_put.status_code != 200:
                                print(f"Failed to update Leader Board: {response_put.text}")
                            if instance.paid == '1':
                                # print("in if for paid")
                                id = instance.id
                                # print("email", instance.id)
                                delete_url = f'https://crm.alnafi.com/api/resource/Daily Sales Module/{id}'
                                delete_response = requests.delete(delete_url, headers=headers)
                                # print(delete_response)
                                print(f"Lead with email {id} deleted. Response: {delete_response.text}")
                                try:
                                    daily_lead_instance = Daily_lead.objects.get(id=instance.id)
                                    Deleted_Daily_lead.objects.create(
                                        crm_id=daily_lead_instance.id,
                                        email=daily_lead_instance.email,
                                        phone=daily_lead_instance.phone,
                                        status=daily_lead_instance.status,
                                        product=daily_lead_instance.product,
                                        plan=daily_lead_instance.plan,
                                        renewal=daily_lead_instance.renewal,
                                        is_exam_fee=daily_lead_instance.is_exam_fee,
                                        amount=daily_lead_instance.amount,
                                        source=daily_lead_instance.source,
                                        lead_creator=daily_lead_instance.lead_creator,
                                        manager_approval=daily_lead_instance.manager_approval,
                                        manager_approval_crm=daily_lead_instance.manager_approval_crm,
                                        veriification_cfo=daily_lead_instance.veriification_cfo,
                                        support=daily_lead_instance.support,
                                        completely_verified=daily_lead_instance.completely_verified,
                                        paid=daily_lead_instance.paid,
                                        is_comission = daily_lead_instance.is_comission,
                                        created_at=daily_lead_instance.created_at,
                                    )
                                    # Delete the instance from Daily_lead
                                    daily_lead_instance.delete()
                                except:
                                    pass
            except Exception as e:
                print(f"Error occurred while deducting from Leader Board: {str(e)}")
    else:
        print("Commission not created")


# @receiver(post_delete, sender=Daily_lead)
def deduct_from_leader_board_on_delete(sender, instance, **kwargs):
    print("delete signal running")
    # print("veriification_cfo", instance.veriification_cfo)
    # if instance.veriification_cfo == 'Deduct Commission Due Some Cause':
    if instance.paid == '0' and instance.completely_verified == 'true':
        try:
            lead_creator = instance.lead_creator
            # print("instance.lead_creator",  lead_creator)
            if lead_creator:
                amount_to_deduct = float(instance.amount)
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
                change = amount - conversion
                gst_tax = change*0.13
                total_amount = round(change-gst_tax)
                # usd_amount = total_amount
                # print("total", total_amount)           
            else:
                amount = float(instance.amount)
                gst_tax = amount*0.05
                total_amount = round(amount-gst_tax)
                # print("total", total_amount)

            if instance.support.lower() == 'true':
                comission_amount = total_amount*0.02
            else:
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


            # print("amont", amount_to_deduct)
            url_get = 'https://crm.alnafi.com/api/resource/Leader Board For Sales?fields=["*"]'
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
                response_data = response_get.json()
                # print("response data", response_data)
                for lead_entry in response_data['data']:
                    if lead_entry.get('lead_owner') == lead_creator:
                        # print("Owner", lead_entry.get('lead_owner'))
                        # print(lead_entry.get('earn_usd_commission'))
                        # print(lead_entry.get('total_usd_revenue'))
                        payload = {}
                        if instance.source in ['dlocal', 'Stripe']:
                            payload["earn_usd_commission"] = max(round(float(lead_entry.get('earn_usd_commission', 0)) - comission_amount), 0)
                            payload["total_usd_revenue"] = max(round(float(lead_entry.get('total_usd_revenue', 0)) - amount_to_deduct), 0)
                        else:
                            payload["earn_pkr_commission"] = max(round(float(lead_entry.get('earn_pkr_commission', 0)) - comission_amount), 0)
                            payload["total_revenue"] = max(round(float(lead_entry.get('total_revenue', 0)) - amount_to_deduct), 0)
                        # print("payload", payload)
                        url_put = f'https://crm.alnafi.com/api/resource/Leader Board For Sales/{lead_entry["name"]}'
                        response_put = requests.put(url_put, headers=headers, json=payload)
                        if response_put.status_code != 200:
                            print(f"Failed to update Leader Board: {response_put.text}")
        except Exception as e:
            print(f"Error occurred while deducting from Leader Board: {str(e)}")
    else:
        print("Not Deducted")


@receiver(post_save, sender=Daily_Sales_Support)
def commission_making_support(sender, instance, created, **kwargs):
    thread = Thread(target=on_support_saved, args=(sender, instance, created), kwargs=kwargs)
    thread.start()
def on_support_saved(sender, instance, created, **kwargs):
    # print("signal running")
    if instance.pk is None:
        return
    if instance.manager_approval == 'True' and instance.manager_approval_crm == 'True' and instance.veriification_cfo == 'True' and instance.completely_verified == '1' and instance.paid == '0':
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
            change = amount - conversion
            gst_tax = change*0.13
            total_amount = round(change-gst_tax)
            # usd_amount = total_amount
            # print("total", total_amount)           
        else:
            amount = float(instance.amount)
            gst_tax = amount*0.05
            total_amount = round(amount-gst_tax)
            # print("total", total_amount)


            
        if instance.is_exam_fee is not None and instance.is_exam_fee.lower() == 'true':
            comission_amount = total_amount*0
        else:
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
                existing_usd_revenue = float(existing_lead.get('total_usd_revenue', 0))
                # print("Existing", existing_amount)
                instance_amount = float(instance.amount)
                payload = {
                    "earn_pkr_commission": round(comission_amount + existing_earn_pkr) if instance.source not in ['Stripe', 'dlocal'] else existing_earn_pkr,
                    "earn_usd_commission": round(comission_amount + existing_earn_usd) if instance.source in ['Stripe', 'dlocal'] else existing_earn_usd,
                    "total_revenue": round(instance_amount + existing_amount) if instance.source not in ['Stripe', 'dlocal'] else existing_amount,
                    "total_usd_revenue": round(instance_amount + existing_usd_revenue) if instance.source in ['Stripe', 'dlocal'] else existing_usd_revenue,
                    # Add other fields you want to update
                }
                response_put = requests.put(url_put, headers=headers, json=payload)
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
                url = "https://crm.alnafi.com/api/resource/Leader Board For Support"
                response = requests.post(url, headers=headers, json=payload)
                # print(response.status_code)
                # print(response.text)
                # return response("Done")
    else:
        print("Not Verified")


@receiver(post_save, sender=Daily_Sales_Support)
def commission_deduction_support(sender, instance, **kwargs):
    thread = Thread(target=deduct_from_leader_board_support, args=(sender, instance), kwargs=kwargs)
    thread.start()
def deduct_from_leader_board_support(sender, instance, **kwargs):
    # print("signal running")
    # print("veriification_cfo", instance.veriification_cfo)
    print("instance.is_comission",instance.is_comission)
    if instance.is_comission:
        if instance.veriification_cfo == 'Deduct Commission Due Some Cause' or instance.paid == '1':
            try:
                lead_creator = instance.lead_creator
                # print("instance.lead_creator",  lead_creator)
                if lead_creator:
                    amount_to_deduct = float(instance.amount)
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
                    change = amount - conversion
                    gst_tax = change*0.13
                    total_amount = round(change-gst_tax)
                    # usd_amount = total_amount
                    # print("total", total_amount)           
                else:
                    amount = float(instance.amount)
                    gst_tax = amount*0.05
                    total_amount = round(amount-gst_tax)
                    # print("total", total_amount)
                comission_amount = total_amount*0.02
                # print("amont", amount_to_deduct)
                url_get = 'https://crm.alnafi.com/api/resource/Leader Board For Support?fields=["*"]'
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
                    response_data = response_get.json()
                    # print("response data", response_data)
                    for lead_entry in response_data['data']:
                        if lead_entry.get('lead_owner') == lead_creator:
                            # print("Owner", lead_entry.get('lead_owner'))
                            # print(lead_entry.get('earn_usd_commission'))
                            # print(lead_entry.get('total_usd_revenue'))
                            payload = {}
                            if instance.source in ['dlocal', 'Stripe']:
                                payload["earn_usd_commission"] = max(round(float(lead_entry.get('earn_usd_commission', 0)) - comission_amount), 0)
                                payload["total_usd_revenue"] = max(round(float(lead_entry.get('total_usd_revenue', 0)) - amount_to_deduct), 0)
                            else:
                                payload["earn_pkr_commission"] = max(round(float(lead_entry.get('earn_pkr_commission', 0)) - comission_amount), 0)
                                payload["total_revenue"] = max(round(float(lead_entry.get('total_revenue', 0)) - amount_to_deduct), 0)
                            # print("payload", payload)
                            url_put = f'https://crm.alnafi.com/api/resource/Leader Board For Support/{lead_entry["name"]}'
                            response_put = requests.put(url_put, headers=headers, json=payload)
                            if response_put.status_code != 200:
                                print(f"Failed to update Leader Board: {response_put.status_code}")
                            if instance.paid == '1':
                                # print("in if for paid")
                                id = instance.id
                                # print("email", instance.id)
                                delete_url = f'https://crm.alnafi.com/api/resource/Daily Sales For Support/{id}'
                                delete_response = requests.delete(delete_url, headers=headers)
                                # print(delete_response)
                                print(f"Lead with email {id} deleted. Response: {delete_response.text}")
                                # try:
                                daily_Support_instance = Daily_Sales_Support.objects.get(id=instance.id)
                                Deleted_Daily_Sales_Support.objects.create(
                                    crm_id=daily_Support_instance.id,
                                    email=daily_Support_instance.email,
                                    phone=daily_Support_instance.phone,
                                    status=daily_Support_instance.status,
                                    product=daily_Support_instance.product,
                                    plan=daily_Support_instance.plan,
                                    is_exam_fee=daily_Support_instance.is_exam_fee,
                                    amount=daily_Support_instance.amount,
                                    source=daily_Support_instance.source,
                                    lead_creator=daily_Support_instance.lead_creator,
                                    manager_approval=daily_Support_instance.manager_approval,
                                    manager_approval_crm=daily_Support_instance.manager_approval_crm,
                                    veriification_cfo=daily_Support_instance.veriification_cfo,
                                    completely_verified=daily_Support_instance.completely_verified,
                                    paid=daily_Support_instance.paid,
                                    is_comission=daily_Support_instance.is_comission,
                                    created_at=daily_Support_instance.created_at,
                                )
                                # Delete the instance from Daily_lead
                                daily_Support_instance.delete()
                                # except:
                                    # pass
            except Exception as e:
                print(f"Error occurred while deducting from Leader Board: {str(e)}")
    else:
        print("commision support not created")

        
# @receiver(post_delete, sender=Daily_Sales_Support)
def deduct_from_leader_board_support_on_delete(sender, instance, **kwargs):
    # print("signal running")
    # print("veriification_cfo", instance.veriification_cfo)
    if instance.paid == '0' and instance.completely_verified == 'true':
        try:
            lead_creator = instance.lead_creator
            # print("instance.lead_creator",  lead_creator)
            if lead_creator:
                amount_to_deduct = float(instance.amount)
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
                change = amount - conversion
                gst_tax = change*0.13
                total_amount = round(change-gst_tax)
                # usd_amount = total_amount
                # print("total", total_amount)           
            else:
                amount = float(instance.amount)
                gst_tax = amount*0.05
                total_amount = round(amount-gst_tax)
                # print("total", total_amount)
            comission_amount = total_amount*0.02
            # print("amont", amount_to_deduct)
            url_get = 'https://crm.alnafi.com/api/resource/Leader Board For Support?fields=["*"]'
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
                response_data = response_get.json()
                # print("response data", response_data)
                for lead_entry in response_data['data']:
                    if lead_entry.get('lead_owner') == lead_creator:
                        # print("Owner", lead_entry.get('lead_owner'))
                        # print(lead_entry.get('earn_usd_commission'))
                        # print(lead_entry.get('total_usd_revenue'))
                        payload = {}
                        if instance.source in ['dlocal', 'Stripe']:
                            payload["earn_usd_commission"] = max(round(float(lead_entry.get('earn_usd_commission', 0)) - comission_amount), 0)
                            payload["total_usd_revenue"] = max(round(float(lead_entry.get('total_usd_revenue', 0)) - amount_to_deduct), 0)
                        else:
                            payload["earn_pkr_commission"] = max(round(float(lead_entry.get('earn_pkr_commission', 0)) - comission_amount), 0)
                            payload["total_revenue"] = max(round(float(lead_entry.get('total_revenue', 0)) - amount_to_deduct), 0)
                        # print("payload", payload)
                        url_put = f'https://crm.alnafi.com/api/resource/Leader Board For Support/{lead_entry["name"]}'
                        response_put = requests.put(url_put, headers=headers, json=payload)
                        if response_put.status_code != 200:
                            print(f"Failed to update Leader Board: {response_put.status_code}")
        except Exception as e:
            print(f"Error occurred while deducting from Leader Board: {str(e)}")